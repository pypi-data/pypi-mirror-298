from __future__ import annotations

import base64
import os
from typing import List, Tuple
from typing import List, Iterable, Tuple

import pandas as pd
import tqdm
from wisecube_sdk import api_calls, create_payload, create_response, string_query
from wisecube_sdk.model_formats import WisecubeModel, OutputFormat
from wisecube_sdk.node_types import NodeType
import json



class WisecubeClient:
    def __init__(self, *args):
        if len(args) == 0:
            open_url = "http://127.0.0.1:5000/api/endpoint"
            self.client = OpenClient(open_url)
        elif len(args) == 1:
            self.client = ApiClient(*args)
        elif len(args) == 3:
            self.client = AuthClient(*args)
        else:
            raise Exception("Invalid args")

def fix_qid(qid: str | Iterable[str]) -> List[str]:
    """
    this function normalizes entity URLs to QIDs
    :param qid: a Wikidata QID or entity URL (wd:Q123), or an `Iterable` of such
    :returns: a list of QIDs
    """
    if isinstance(qid, str):
        qid = [qid]
    fixed = []
    for q in qid:
        if q.startswith("http://www.wikidata.org/entity/"):
            fixed.append(q.split("/")[-1])
        else:
            fixed.append(q)
    return fixed


def fix_pred(pred: str | Iterable[str]) -> List[str]:
    """
    this function normalizes predicate URLs to predicate IDs
    :param pred: a Wikidata predicate ID or predicate URL (wdt:P123), or an `Iterable` of such
    :returns: a list of predicate IDs
    """
    if isinstance(pred, str):
        pred = [pred]
    fixed = []
    for p in pred:
        if p.startswith("http://www.wikidata.org/prop/direct/"):
            fixed.append(p.split("/")[-1])
        else:
            fixed.append(p)
    return fixed

class QueryMethods:
    def __init__(self, url, client_id):
        self.url = url
        self.client_id = client_id


    @property
    def output_format(self):
        return getattr(self, '_output_format', OutputFormat.JSON)

    @output_format.setter
    def output_format(self, value):
        if not isinstance(value, OutputFormat):
            raise ValueError("output_format must be a OutputFormat.")
        self._output_format = value

    def get_headers(self):
        raise NotImplementedError("Subclasses must implement get_headers")

    def search_qid(self, text):
        variables = {
            "question": text
        }
        payload = create_payload.create(string_query.search_qids, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_qids(response)


    def search_by_type(self,type_qid: str, name: str | None = None, include_instances: bool = True,
                       include_subclasses: bool = False):
        """
        This function searches Wikidata for things that of the "type" provided. In Wikidata, type is not simply an "is-a" relationship.
        There are two main predicates used to define "type", "instance of" (P31) [example `(Garfield, P31, cat)`] and "subclass of" (P279) [example `(cat, P279, mammal)`]
        :param type_qid: a Wikidata QID or entity URL (wd:Q123)
        :param name: an optional name for the `pandas.DataFrame` columns
        :param include_instances: if this flag is true, retrieve instances (P31) of subclasses (P279) of the provided QID (default: True)
        :param include_subclasses: if this flag is true, retrieve subclasses (P279) of the provided QID (default: False)
        :returns: a `pandas.DataFrame` of the entity URLs and labels
        """

        type_qid = fix_qid(type_qid)[0]
        pred = []
        if include_instances:
            pred.append("(wdt:P31/wdt:P279*)")  # instance of type_qid or some subclass of type_qid
        if include_subclasses:
            pred.append("(wdt:P279*)")  # type_qid or some subclass of type_qid <- includes type_qid
        pred = "|".join(pred)
        query = f"""
      SELECT DISTINCT ?item ?itemLabel
      WHERE {{
        ?item {pred} wd:{type_qid} .
        ?item rdfs:label ?itemLabel. FILTER(LANG(?itemLabel)="en")
      }}
      """
        result = self.advance_search(query)
        if name is not None:
            result = result.rename({"item": name, "itemLabel": f"{name}Label"}, axis=1)
        return result

    def search_by_relationship(self,
            qid: str | Iterable[str], pred: str, incoming: bool = False,
            qid_name: str | None = None, neighbor_name: str | None = None,
            batch_size: int = 100):
        """
        This function searches Wikidata for entities in a particular relationship to provided entities
        :param qid: a Wikidata QID or entity URL (wd:Q123), or an `Iterable` of such
        :param pred: a Wikidata predicate ID
        :param incoming: if this flag is true, the relationship is assumed to be `(neighbor_QID, pred, QID)`, otherwise it is assumed to be `(QID, pred, neighbor_QID)` (default: False)
        :param qid_name: an optional name for the `pandas.DataFrame` columns made from the provided QID(s)
        :param neighbor_name: an optional name for the `pandas.DataFrame` columns made from the neighbors
        :param batch_size: the maximum number of QIDs to search for at once (default: 100)
        :returns: a `pandas.DataFrame` of the entity URLs and labels from the provided QID(s) and URLs and labels for the neighbors found
        """

        qid = fix_qid(qid)
        pred = fix_pred(pred)[0]
        result = pd.DataFrame()
        rel_clause = f"?source wdt:{pred} ?item ."  # incoming
        if incoming:
            rel_clause = f"?item wdt:{pred} ?source ."  # outgoing
        if len(qid) > batch_size:
            iteration = tqdm.trange(0, len(qid), batch_size)
        else:
            iteration = range(0, len(qid), batch_size)
        for i in iteration:
            batch = qid[i:i + batch_size]
            query = f"""
        SELECT DISTINCT ?source ?sourceLabel ?item ?itemLabel
        WHERE {{
          VALUES ?source {{ wd:{" wd:".join(qid)} }}
          {rel_clause}
          ?source rdfs:label ?sourceLabel. FILTER(LANG(?sourceLabel)="en")
          ?item rdfs:label ?itemLabel. FILTER(LANG(?itemLabel)="en")
        }}
        """
            result = pd.concat((result, self.advance_search(query))).reset_index(drop=True)
        if qid_name is not None:
            result = result.rename({"source": qid_name, "sourceLabel": f"{qid_name}Label"}, axis=1)
        if neighbor_name is not None:
            result = result.rename({"item": neighbor_name, "itemLabel": f"{neighbor_name}Label"}, axis=1)
        return result

    def search_by_qualifier(self,
            triples: Tuple[str, str, str] | List[Tuple[str, str, str]],
            qual_pred: str, qual_name: str | None = None,
            sub_name: str | None = None, pred_name: str | None = None, obj_name: str | None = None,
            batch_size: int = 100):
        """
        This function searches Wikidata for entities related by a particular predicate to a triple.
        In Wikidata, the qualifiers are represented by something called reification. The triple is represented by a special statement entity.
        If there is a triple `(wd:Q123, wdt:P456, wd:Q789)`, then the statement `ST` is connected by the following triples
        `(wd:Q123, p:P456, ST)` and `(ST, ps:456, wd:Q789)`
        This function is looking for entities such that `(ST, qual_pred, qual)`
        :param triple: a Wikidata triple `(subject_QID, predicate_ID, object_QID)` or an `Iterable` of such
        :param qual_pred: a Wikidata predicate ID
        :param qual_name: an optional name for the `pandas.DataFrame` columns made from the qualifier entities
        :param sub_name: an optional name for the `pandas.DataFrame` columns made from the subject entities
        :param pred_name: an optional name for the `pandas.DataFrame` columns made from the predicates
        :param obj_name: an optional name for the `pandas.DataFrame` columns made from the object entities
        :param batch_size: the maximum number of QIDs to search for at once (default: 100)
        :returns: a `pandas.DataFrame` of the entity URLs and labels from the provided QID(s) and URLs and labels for the neighbors found
        """

        if isinstance(triples, tuple):
            triples = [triples]
        subjects, predicates, objects = zip(*triples)

        # normalizing
        subjects = fix_qid(subjects)
        predicates = fix_pred(predicates)
        objects = fix_qid(objects)
        qual_pred = fix_pred(qual_pred)[0]

        result = pd.DataFrame()
        if len(triples) > batch_size:
            iteration = tqdm.trange(0, len(triples), batch_size)
        else:
            iteration = range(0, len(triples), batch_size)
        for i in iteration:
            subs = subjects[i:i + batch_size]
            preds = predicates[i:i + batch_size]
            objs = objects[i:i + batch_size]
            # subject, wdt namespace predicate, p namespace predicate, ps namespace predicate, object
            batch = [f"(wd:{s} wdt:{p} p:{p} ps:{p} wd:{o})" for s, p, o in zip(subs, preds, objs)]
            query = f"""
        SELECT DISTINCT ?s ?p ?o ?qual ?qualLabel
        WHERE {{
          VALUES (?s ?p ?pp ?psp ?o) {{ {" ".join(batch)} }}
          ?s ?pp ?st .
          ?st ?psp ?o .
          ?st pq:{qual_pred} ?qual .
          ?qual rdfs:label ?qualLabel. FILTER(LANG(?qualLabel)="en")
        }}
        """
            try:
                result = pd.concat((result, self.advance_search(query))).reset_index(drop=True)
            except KeyError as ke:
                continue
        if qual_name is not None:
            result = result.rename({"qual": qual_name, "qualLabel": f"{qual_name}Label"}, axis=1)
        if sub_name is not None:
            result = result.rename({"s": sub_name}, axis=1)
        if pred_name is not None:
            result = result.rename({"p": pred_name}, axis=1)
        if obj_name is not None:
            result = result.rename({"o": obj_name}, axis=1)
        return result

    def search_by_domain(self,qid: str | Iterable[str], batch_size: int = 100):
        """
        This function searches for a predicate with (one of) the provided QID as its domain
        :param qid: a Wikidata QID or entity URL (wd:Q123), or an `Iterable` of such
        :returns: a `pandas.DataFrame` of the domains and predicates
        """
        qid = fix_qid(qid)
        result = pd.DataFrame()
        if len(qid) > batch_size:
            iteration = tqdm.trange(0, len(qid), batch_size)
        else:
            iteration = range(0, len(qid), batch_size)
        for i in iteration:
            batch = qid[i:i + batch_size]
            query = f"""
          PREFIX schema: <http://schema.org/>
          SELECT DISTINCT ?domain ?domainLabel ?predicate ?predicateLabel ?predicateDescription
          WHERE {{
            VALUES ?domain {{ wd:{" wd:".join(batch)} }}
            ?domain rdfs:label ?domainLabel .
            FILTER(LANG(?domainLabel)="en")
            ?predicate p:P2302 ?dst .
            ?dst ps:P2302 wd:Q21503250 .
            ?dst pq:P2308 ?domain .
            ?predicate rdfs:label ?predicateLabel ;
                      schema:description ?predicateDescription .
            FILTER(LANG(?predicateLabel)="en")
            FILTER(LANG(?predicateDescription)="en")
          }}
        """
            try:
                incr = self.advance_search(query)
            except KeyError:
                incr = pd.DataFrame()
            result = pd.concat((result, incr)).reset_index(drop=True)
            result = pd.concat((result, incr), ignore_index=True)
        result["domain"] = result["domain"].str.split("/").str[-1]
        result["predicate"] = result["predicate"].str.split("/").str[-1]
        return result

    def search_by_range(self,qid: str | Iterable[str], batch_size: int = 100):
        """
        This function searches for a predicate with (one of) the provided QID as its range
        :param qid: a Wikidata QID or entity URL (wd:Q123), or an `Iterable` of such
        :returns: a `pandas.DataFrame` of the range and predicates
        """
        qid = fix_qid(qid)
        result = pd.DataFrame()
        if len(qid) > batch_size:
            iteration = tqdm.trange(0, len(qid), batch_size)
        else:
            iteration = range(0, len(qid), batch_size)
        for i in iteration:
            batch = qid[i:i + batch_size]
            query = f"""
          PREFIX schema: <http://schema.org/>
          SELECT DISTINCT ?range ?rangeLabel ?predicate ?predicateLabel ?predicateDescription
          WHERE {{
            VALUES ?range {{ wd:{" wd:".join(batch)} }}
            ?range rdfs:label ?rangeLabel .
            FILTER(LANG(?rangeLabel)="en")
            ?predicate p:P2302 ?rst .
            ?rst ps:P2302 wd:Q21510865 .
            ?rst pq:P2308 ?range .
            ?predicate rdfs:label ?predicateLabel ;
                      schema:description ?predicateDescription .
            FILTER(LANG(?predicateLabel)="en")
            FILTER(LANG(?predicateDescription)="en")
          }}
        """
            try:
                incr = self.advance_search(query)
            except KeyError:
                incr = pd.DataFrame()
            result = pd.concat((result, incr)).reset_index(drop=True)
            result = pd.concat((result, incr), ignore_index=True)
        result["range"] = result["range"].str.split("/").str[-1]
        result["predicate"] = result["predicate"].str.split("/").str[-1]
        return result

    def node_search(self,name: str, ignore_case: bool = True, matching_strategy: str = "FUZZY", limit: int = 10,
                    entities: bool = True):

        """
        This function searches Wikidata for a particular entity or predicate using the MediaWiki API
        :param name: the name for searching
        :param ignore_case: if this flag is true then it will be a case insensitive search (default: False)
        "param matching_strategy: this is how the name is being used to match to candidate entities (default: "FUZZY")
        EXACT - exact match of label and name
        PREFIX - do labels of candidate entities begin with name
        SUFFIX - do labels of candidate entities end with name
        CONTAINS - do labels of candidate entities contain name
        FUZZY - do not filter labels after MediaWiki retrieval
        :param entities: flag to search for entities (True) or predicates (False) (default: True)
        """
        case_clause = f"""BIND(?label AS ?matchLabel)"""
        if ignore_case:
            name = name.lower()
            case_clause = f"""BIND(LCASE(?label) AS ?matchLabel)"""
        match_clause: str
        if matching_strategy == "EXACT":
            match_clause = f"""FILTER(?matchLabel = "{name}"@en)"""
        elif matching_strategy == "PREFIX":
            match_clause = f"""FILTER(STRSTARTS(?matchLabel, "{name}"))"""
        elif matching_strategy == "SUFFIX":
            match_clause = f"""FILTER(STRENDS(?matchLabel, "{name}"))"""
        elif matching_strategy == "CONTAINS":
            match_clause = f"""FILTER(CONTAINS(?matchLabel, "{name}"))"""
        elif matching_strategy == "FUZZY":
            match_clause = ""
        else:
            raise ValueError(f"unrecognized matching strategy [{matching_strategy}]")
        if entities:
            ents_or_preds = ""
            cui_clause = "?item wdt:P2892 ?cui ."
            cui_select = "?cui"
        elif not entities:
            ents_or_preds = 'mwapi:type "property"'
            cui_clause = ""
            cui_select = ""
        query = f"""
      PREFIX bd: <http://www.bigdata.com/rdf#>
      PREFIX mwapi: <https://www.mediawiki.org/ontology#API/>
      PREFIX schema: <http://schema.org/>
      PREFIX wikibase: <http://wikiba.se/ontology#>
      SELECT DISTINCT ?item {cui_select} ?label ?description
      WHERE {{
        SERVICE wikibase:mwapi {{
          bd:serviceParam wikibase:endpoint "www.wikidata.org" ;
                          wikibase:api "EntitySearch" ;
                          mwapi:search "{name}" ;
                          mwapi:language "en" ;
                          mwapi:limit "{max(20, limit)}" ;
                          {ents_or_preds} .
            ?item wikibase:apiOutputItem mwapi:item.
            ?num wikibase:apiOrdinal true.
        }}
        FILTER(LANG(?label)="en")
        {cui_clause}
        ?item rdfs:label ?label ;
              schema:description ?description .
        FILTER(LANG(?description)="en")
        {case_clause}
        {match_clause}
      }}
      ORDER BY ?num
      """
        try:
            df = self.advance_search(query).iloc[:limit]
            df["item"] = df["item"].str.split("/").str[-1]
            return df.iloc[:limit]
        except KeyError as ke:
            return

    def search_predicates(self,qid: str | Iterable[str], relationships: bool = True, properties: bool = False,
                       incoming: bool = False, batch_size: int = 100):
        """
        This function retrieves the predicates attached to the given QID(s)
        :param qid: a Wikidata QID or entity URL (wd:Q123), or an `Iterable` of such
        :param relationships: if this flag is true, retrieve the relationships (entity-to-entity) (default:True)
        :param properties: if this flag is true, retrieve the properties (entity-to-literal) (default: False)
        :param incoming: if this flag is true, the relationship is assumed to be `(neighbor_QID, pred, QID)`, otherwise it is assumed to be `(QID, pred, neighbor_QID)` (default: False)
        :returns: a `pandas.DataFrame` of the entity URLs and predicates
        """
        if properties and incoming:
            raise ValueError("properties are only outgoing")
        qid = fix_qid(qid)
        result = pd.DataFrame()
        triple_clause = "?item ?predicate ?x"
        rel_clause = "FILTER(!ISURI(?x))"
        prop_clause = "FILTER(!ISLITERAL(?x))"
        if relationships:
            rel_clause = ""
            if incoming:
                triple_clause = "?x ?predicate ?item"
        if properties:
            prop_clause = ""
        if len(qid) > batch_size:
            iteration = tqdm.trange(0, len(qid), batch_size)
        else:
            iteration = range(0, len(qid), batch_size)
        for i in iteration:
            batch = qid[i:i + batch_size]
            query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX wikibase: <http://wikiba.se/ontology#>
        SELECT DISTINCT ?item ?itemLabel ?predicate ?predicateLabel ?predicateDescription
        WHERE {{
          VALUES ?item {{ wd:{" wd:".join(batch)} }}
          {triple_clause} .
          {rel_clause}
          {prop_clause}
          ?wdpred wikibase:directClaim ?predicate ;
                  rdfs:label ?predicateLabel ;
                  schema:description ?predicateDescription .
          FILTER(LANG(?predicateLabel)="en")
          FILTER(LANG(?predicateDescription)="en")
          ?item rdfs:label ?itemLabel .
          FILTER(LANG(?itemLabel)="en")
        }}
        """
            try:
                incr = self.advance_search(query)
            except KeyError:
                incr = pd.DataFrame()
            result = pd.concat((result, incr)).reset_index(drop=True)
            result = pd.concat((result, incr), ignore_index=True)
        result = result.sort_values(["itemLabel", "predicateLabel"])
        result["item"] = result["item"].str.split("/").str[-1]
        result["predicate"] = result["predicate"].str.split("/").str[-1]
        result = result.reset_index(drop=True)
        return result

    def get_predicate_info(self,predicate: str):
        """
        This function retrieves the info on a given predicate
        :param predicate: a Wikidata predicate ID or predicate URL (e.g. P31)
        :reurns: a `pandas.Series` of the predicates and their info
        """
        predicate = fix_qid(predicate)[0]
        occ_query = f"""
      SELECT DISTINCT ?predicate (COUNT(DISTINCT ?statement) AS ?occurrences)
      WHERE {{
        BIND(p:{predicate} AS ?predicate)
        ?s ?predicate ?statement .
      }}
      GROUP BY ?predicate
      """
        try:
            occs = self.advance_search(occ_query)
            occs = occs["occurrences"].iloc[0]
        except KeyError:
            occs = 0
        name_desc_query = f"""
      PREFIX schema: <http://schema.org/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
      PREFIX wikibase: <http://wikiba.se/ontology#>
      SELECT DISTINCT ?predicate ?predicateLabel ?predicateDescription (GROUP_CONCAT(?predicateAlias; separator=";") AS ?predicateAliases)
      WHERE {{
        BIND(wd:{predicate} AS ?predicate)
        ?predicate rdfs:label ?predicateLabel ;
                  schema:description ?predicateDescription .
        OPTIONAL {{
          ?predicate skos:altLabel ?predicateAlias .
        }}
        FILTER(LANG(?predicateLabel)="en")
        FILTER(LANG(?predicateDescription)="en")
        FILTER(LANG(?predicateAlias)="en")
      }}
      GROUP BY ?predicate ?predicateLabel ?predicateDescription
      """
        try:
            name_desc = self.advance_search(name_desc_query)
            predicateLabel = name_desc["predicateLabel"].iloc[0]
            predicateDescription = name_desc["predicateDescription"].iloc[0]
            predicateAliases = name_desc["predicateAliases"].iloc[0]
        except KeyError:
            predicateLabel = ""
            predicateDescription = ""
            predicateAliases = ""
        constraint_query = f"""
      SELECT DISTINCT ?predicate ?domain ?domainLabel ?range ?rangeLabel
      WHERE {{
        BIND(wd:{predicate} AS ?predicate)
        OPTIONAL {{
          ?predicate p:P2302 ?dst .
          ?dst ps:P2302 wd:Q21503250 .
          ?dst pq:P2308 ?domain .
          ?domain rdfs:label ?domainLabel .
          FILTER(LANG(?domainLabel)="en")
        }}
        OPTIONAL {{
          ?predicate p:P2302 ?rst .
          ?rst ps:P2302 wd:Q21510865 .
          ?rst pq:P2308 ?range .
          ?range rdfs:label ?rangeLabel .
          FILTER(LANG(?rangeLabel)="en")
        }}
      }}
      """
        try:
            domain = {}
            range = {}
            constraints = self.advance_search(constraint_query)
            for _, (_, d, dl, r, rl) in constraints.iterrows():
                if d:
                    domain[d.split("/")[-1]] = dl
                if r:
                    range[r.split("/")[-1]] = rl
        except KeyError:
            domain = {}
            range = {}
        return pd.Series({
            "predicate": predicate,
            "predicateLabel": predicateLabel,
            "predicateDescription": predicateDescription,
            "predicateAliases": predicateAliases,
            "occurrences": occs,
            "domain": domain,
            "range": range,
        })



    def search_entities(self, name,ignore_case=False, matching_strategy=None,limit=None):
        variables = {
            "name": name
        }
        if ignore_case is None:
            variables["ignoreCase"] = False
        else:
            variables["ignoreCase"] = ignore_case
        if matching_strategy is None:
            variables["matchingStrategy"] = "FUZZY"
        else:
            variables["matchingStrategy"] = matching_strategy

        if limit is None:
            variables["limit"] = 10
        else:
            variables["limit"]=limit

        payload = create_payload.create(string_query.search_entities, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_entities(response,self.output_format)

    def search_predicate(self, name,ignore_case=True, matching_strategy=None,limit=None):
        variables = {
            "name": name,
            "ignoreCase": ignore_case if ignore_case is not None else True,
            "matchingStrategy": matching_strategy if matching_strategy is not None else "CONTAINS",
            "limit": limit if limit is not None else 10

        }

        payload = create_payload.create(string_query.search_predicate, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_predicate(response,self.output_format)



    def qa(self, text):
        variables = {
            "query": text
        }
        payload = create_payload.create(string_query.qa, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.qa(response, self.output_format)

    def documents(self, text):
        variables = {
            "query": text
        }
        payload = create_payload.create(string_query.documents, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.documents(response, self.output_format)

    def search_graph(self, text, nr=10, node_types: List[NodeType] = None):
        if create_payload.is_valid_url(text):
            variables = {
                "maxNeighbours": nr,
                "startNode": text
            }
        else:
            variables = {
                "maxNeighbours": nr,
                "startNodeName": text
            }

        if node_types is not None:
            node_type_names = [node_type.name for node_type in node_types]
            variables["nodeTypes"] = node_type_names

        payload = create_payload.create(string_query.search_graph, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_graph(response, self.output_format)

    def search_text(self, text):
        variables = {
            "query": text
        }
        payload = create_payload.create(string_query.search_text, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_text(response, self.output_format)

    def execute_vector_function(self, graphIds: [str]):
        variables = {
            "graphIds": graphIds
        }
        payload = create_payload.create(string_query.execute_vector_function, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        if response is not None:
            return create_response.execute_vector_function(response, self.output_format)
        return []

    def execute_score_function(self, graphIds: [[str]]):
        variables = {
            "triples": graphIds
        }
        payload = create_payload.create(string_query.execute_score_function, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.execute_score_function(response, self.output_format)

    def nl_to_sparql(self, question: str):
        variables = {
            "question": question
        }
        payload = create_payload.create(string_query.execute_nl2sparql, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.nl_2_sparql(response)

    def get_predicates(self, label: str):
        variables = {
            "label": label
        }
        payload = create_payload.create(string_query.get_predicates, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.get_predicates(response, self.output_format)

    def advance_search(self, query: str):
        variables = {
            "query": query
        }
        payload = create_payload.create(string_query.advanced_search_query, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.advanced_search(response, self.output_format)

    def get_admet_predictions(self, smiles: [str], model: WisecubeModel):
        variables = {
            "smiles": smiles,
            "modelName": model.value
        }
        payload = create_payload.create(string_query.get_admet_prediction, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.basic(response)

    def ask_pythia(self, references: [str], response: str, question: str, include_default_validators=False):

        variables = {
            "reference": references,
            "response": response
        }
        if question is not None:
            variables["question"] = question
        if include_default_validators is None:
            variables["includeDefaultValidators"] = False
        else:
            variables["includeDefaultValidators"] = include_default_validators


        payload = create_payload.create(string_query.ask_pythia, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.basic(response)


    def get_pathing(self, scoring):
        pathing = {}
        for _, (index, idxmax) in scoring[["index", "idxmax"]].iterrows():
            pathing[(index, idxmax)] = []
            if index == idxmax:
                pathing[(index, idxmax)] = None
                continue
            for len1_query in string_query.length_1_queries:
                try:
                    len1_query = len1_query.replace("INDEX", index).replace("IDXMAX", idxmax)
                    len1_results = self.advance_search(len1_query)
                    pathing[(index, idxmax)] += len1_results[["dir", "predLabel", "dir"]].apply(" ".join,
                                                                                                axis=1).to_list()
                except KeyError:
                    pass
            for len2_query in string_query.length_2_queries:
                try:
                    len2_query = len2_query.replace("INDEX", index).replace("IDXMAX", idxmax)
                    len2_results = self.advance_search(len2_query)
                    pathing[(index, idxmax)] += len2_results[
                        ["dir1", "pred1Label", "dir1", "nLabel", "dir2", "pred2Label", "dir2"]].apply(" ".join,
                                                                                                      axis=1).to_list()
                except KeyError:
                    pass
        return pathing

class OpenClient:
    def __init__(self, url):
        self.url = url


class AuthClient(QueryMethods):
    def __init__(self, username, password, ):
        super().__init__("https://api.wisecube.ai/orpheus/graphql", "1mbgahp6p36ii1jc851olqfhnm")
        self.username = username
        self.password = password

    def create_token(self):
        payload = {
            "AuthParameters": {
                "USERNAME": self.username,
                "PASSWORD": self.password
            },
            "AuthFlow": "USER_PASSWORD_AUTH",
            "ClientId": self.client_id
        }
        headers = {"X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
                   "Content-Type": "application/x-amz-json-1.1"
                   }
        cognito_url = "https://cognito-idp.us-east-2.amazonaws.com/"

        response = api_calls.create_api_call(payload, headers, cognito_url, "json")

        token = json.loads(response.text)["AuthenticationResult"]["AccessToken"]

        return token

    def get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.create_token()),
            'Content-Type': 'application/json',
        }



class ApiClient(QueryMethods):
    def __init__(self, api_key):
        super().__init__("https://api.wisecube.ai/orpheus/graphql", "1mbgahp6p36ii1jc851olqfhnm")
        self.api_key = api_key

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }


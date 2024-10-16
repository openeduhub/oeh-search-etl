

import logging
import sqlite3
from typing import NamedTuple, Optional

# import sqlparse

log = logging.getLogger(__name__)


class FilterRule(NamedTuple):
    id: int
    rule: str
    include: bool
    position: int

class CrawledUrl(NamedTuple):
    url: str
    page_type: str

# Function to generate the sequential filter string and corresponding parameters
def generate_url_filter(filter_rules: list[FilterRule]) -> tuple[str, list[str]]:
    conditions = []
    parameters = []

    for i, rule in enumerate(filter_rules):
        # log.info("Filter rule pos %d: %s (include: %s)", rule.position, rule.rule, "True" if rule.include else "False")
        if not rule.include:
            continue

        rule_parameters = []

        # handle previous rules
        subconditions = []
        for prev_rule in filter_rules[:i]:
            if not prev_rule.include:
                subconditions.append("cu.url NOT LIKE ?")
                rule_parameters.append(prev_rule.rule + '%')
        
        # handle this rule
        rule_condition = "cu.url LIKE ?"
        rule_parameters.append(rule.rule + '%')

        if subconditions:
            combined_condition = "(" + " AND ".join(subconditions) + f" AND {rule_condition})"
            # combined_condition += " /* Rule pos %d */" % rule.position
            conditions.append(combined_condition)
        else:
            # rule_condition += " /* Rule pos %d */" % rule.position
            conditions.append(rule_condition)
        
        parameters.extend(rule_parameters)

    if not conditions:
        return "1=0", []

    # Combine all conditions with OR
    url_filter = " OR ".join(conditions)
    return url_filter, parameters


def fetch_urls_passing_filterset(connection: sqlite3.Connection, filter_set_id: int,
                                 limit: Optional[int] = None):
    log.info("Filter set ID: %s", filter_set_id)
    # List filter rules in this filter set
    cursor = connection.cursor()

    # Get crawl job id
    cursor.execute("SELECT crawl_job_id FROM crawls_filterset WHERE id = ?", (filter_set_id,))
    row = cursor.fetchone()
    crawl_job_id = row[0]
    log.info("Crawl job ID: %s", crawl_job_id)

    # table: crawls_filterset, crawls_filterrule
    cursor.execute("SELECT id, rule, include, position FROM crawls_filterrule WHERE filter_set_id = ? ORDER BY position ASC", (filter_set_id,))
    filter_rules = cursor.fetchall()
    log.info("Filter rules: %s", filter_rules)

    # expressions = []
    # params = []
    # for row in filter_rules:
    #     rule_id, rule, include, position = row
    #     log.info("Filter rule pos %d: %s (include: %s)", position, rule, "True" if include else "False")
    #     # expression is "url LIKE '%{rule}'"
    #     expressions.append("url LIKE ?")
    #     params.append(f"{rule}%")
    
    # if expressions:
    #     filter_expression = " OR ".join(expressions)
    # else:
    #     filter_expression = "1=1"
    filter_rules = [FilterRule(*rule) for rule in filter_rules]
    # filter_rules = map(FilterRule._make, filter_rules)
    filter_expression, params = generate_url_filter(filter_rules)

   
    # expressions.append("crawl_job_id == ?")
    # params.append(crawl_job_id)
    # where_clause = "WHERE (" + filter_expression + ") AND crawl_job_id = ?"
    # params.append(crawl_job_id)
    if limit:
        assert isinstance(limit, int)
    
    query = f"""
    SELECT 
        cu.url, 
        fr.page_type
    FROM 
        crawls_crawledurl cu
    JOIN 
        crawls_crawljob cj ON cu.crawl_job_id = cj.id
    JOIN 
        crawls_filterset fs ON cj.id = fs.crawl_job_id
    JOIN 
        crawls_filterrule fr ON fs.id = fr.filter_set_id
    WHERE 
        ({filter_expression}) AND 
        fr.include = 1 AND
        fs.id = ? AND
        fr.position = (
            SELECT MIN(position)
            FROM crawls_filterrule AS fr_inner
            WHERE fr_inner.filter_set_id = fs.id 
            AND fr_inner.include = 1
            AND cu.url LIKE (fr_inner.rule || '%')
        )
        {f"LIMIT {limit}" if limit else ""};
    """
    params.append(str(filter_set_id))
    
    #query = "SELECT url FROM crawls_crawledurl AS cu " + where_clause
    log.info("Query: %s", query)
    log.info("Params: %s", params)

    # debug_query = debug_generate_query(query, params)
    # log.info("Debug query: \n%s", sqlparse.format(debug_query, reindent=True, keyword_case='upper'))

    cursor.execute(query, params)

    urls = cursor.fetchall()
    log.info("URLs found: %s", urls)
    cursor.close()
    
    return [CrawledUrl(*row) for row in urls]

def debug_generate_query(query: str, params: str) -> str:
    """ Inserts the parameters into a prepared statement for debugging.
        Each parameter replaces a question mark in the query.
        Do not actually execute the resulting query, it is not safe! """
    for param in params:
        query = query.replace("?", repr(param), 1)
    return query
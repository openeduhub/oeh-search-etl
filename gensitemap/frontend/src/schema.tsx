
export type Rule = {
  id: number;
  rule: string;
  count: number;
  cumulative_count: number;
  include: boolean;
  page_type: string;
  position: number;
};

export type CrawlJob = {
  id: number;
  url_count: number;
  start_url: string;
  follow_links: boolean;
  created_at: string;
  updated_at: string;
};

export type FilterSet = {
  id: number
  crawl_job: CrawlJob
  remaining_urls: number
  name: string
  created_at: string
  updated_at: string
  url: string
  rules: Rule[]
}

// API Responses

export type UnmatchedResponse = {
  is_complete: boolean;
  total_count: number;
  unmatched_urls: string[];
}
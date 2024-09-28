from typing import Any

from fastapi import APIRouter
from sqlmodel import func, select

from mtmai.core.logging import get_logger
from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.models.search_index import SearchIndex, SearchIndexResponse, SearchRequest

router = APIRouter()
logger = get_logger()
sql_schema = """
CREATE TABLE search_index (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,  -- 'site', 'thread', 'task' 等
    title TEXT NOT NULL,
    content TEXT,
    url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector
);

CREATE INDEX search_vector_idx ON search_index USING GIN (search_vector);
"""
# 创建一个触发器函数来自动更新 search_vector：
sql_trigger = """
CREATE FUNCTION search_vector_update() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'B');
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER search_vector_update
BEFORE INSERT OR UPDATE ON search_index
FOR EACH ROW EXECUTE FUNCTION search_vector_update();
"""


@router.post("/", response_model=SearchIndexResponse)
async def search(
    session: AsyncSessionDep, current_user: CurrentUser, req: SearchRequest
) -> Any:
    """
    综合搜索, 支持搜索站点, 文档, 知识库。返回搜索结果的摘要条目。
    前端，通常点击条目后，打开详细操作页
    参考： https://www.w3cschool.cn/article/34124192.html
    """
    search_query = req.q
    offset = req.skip
    limit = req.limit

    query = select(SearchIndex).where(
        # to_tsvector
        func.to_tsvector("english", SearchIndex.title + " " + SearchIndex.content).op(
            "@@"
        )(func.plainto_tsquery("english", search_query))
    )
    query = query.offset(offset).limit(limit)

    result = await session.exec(query)
    items = result.all()
    logger.info("搜索结果 %s", result)
    # 查询搜索索引
    # index_sql = text("""
    # SELECT id, type, title,
    #        ts_headline('english', content, plainto_tsquery(:query)) as snippet,
    #        url,
    #        ts_rank(search_vector, plainto_tsquery(:query)) as rank
    # FROM search_index
    # WHERE search_vector @@ plainto_tsquery(:query)
    # """)

    # # 查询原始表（这里以 sites 表为例）
    # sites_sql = text("""
    # SELECT id, 'site' as type, title,
    #        left(description, 200) as snippet,
    #        url,
    #        0 as rank
    # FROM sites
    # WHERE to_tsvector('english', title || ' ' || description) @@ plainto_tsquery(:query)
    # AND id NOT IN (SELECT id FROM search_index WHERE type = 'site')
    # """)

    # # 执行查询
    # index_result = await session.exec(index_sql, {"query": query})
    # sites_result = await session.exec(sites_sql, {"query": query})

    # # 合并结果
    # all_items = [dict(row) for row in index_result.mappings()] + [dict(row) for row in sites_result.mappings()]

    # # 排序和分页
    # sorted_items = sorted(all_items, key=lambda x: x['rank'], reverse=True)
    # paginated_items = sorted_items[offset:offset+limit]

    # items = [SearchResultItem(**item) for item in paginated_items]

    # # 计算总数
    # total = len(all_items)
    # total_pages = (total + request.per_page - 1) // request.per_page

    return SearchIndexResponse(
        data=items,
        count=len(items),
    )

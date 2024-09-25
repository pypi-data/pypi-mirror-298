from sqlmodel import Session, select


def get_page(
        engine,
        model,
        page: int = 1,
        size: int = 8,
        **query_dict,
):
    """
    查询所有数据
    :param engine: 引擎对象
    :param model: 模型类
    :param page: 第几页
    :param size: 每页数量
    :param query_dict: 查询条件
    """
    with Session(engine) as session:
        # 查询全部
        query = select(model)

        # 等值查询条件
        for k, v in query_dict.items():
            if hasattr(model,k):
                query = query.where(getattr(model,k) == v)

        # 统计个数
        count = len(session.exec(query).all())

        # 根据ID降序
        query = query.order_by(model.id.desc())

        # 分页查询
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        data = session.exec(query).all()

        # 返回
        return {"count": count, "data": data, "page": page, "size": size}
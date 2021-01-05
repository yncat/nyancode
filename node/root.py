class RootNode:
    """プログラム全体を表すノード。"""
    # 必要な引数の型を指定
    parameter_constraints = {}
    # 必要な子ノードを指定
    child_node_constraints = {
        "block"  # 処理本体
    }

# coding:utf-8
# --author-- binglu.wang

import zfused_api
import zfused_maya.core.record as record

def get_assets():
    _assets = {}
    _project_id = record.current_project_id()
    _project_assets = zfused_api.asset.project_assets([_project_id])
    # print _project_assets
    for _asset in _project_assets:
        asset = zfused_api.asset.Asset(_asset["Id"])
        _assets[asset.code()] =asset.production_path()
    return _assets
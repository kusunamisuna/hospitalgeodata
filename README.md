# 病院地理情報取得ツール
- 日本の病院地理情報を取得を行い、TSV・JSON形式にして出力するツール。
- 県コードを指定して、対象の件の病院情報を地理情報付で出力する。
    - データ取得元：http://www.hospital.or.jp/shibu_kaiin/
    - API：'http://www.geocoding.jp/api/

## 使用方法
- `python3 gethospitalgeodata.py {県コード}`

## 参考
- https://github.com/HirotakaAseishi/tokyo_hospitalgeodata

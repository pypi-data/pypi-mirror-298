# common_packages
封装了一些通用的功能

打包
```bash
python -m build
```
安装
```bash
pip install common_packages-0.1.0.tar.gz
```
pypi
https://pypi.org/project/common-packages/#description

依赖
```bash
    "requests",
    'pika',
    "tencentcloud-sdk-python-tmt",
    "kafka-python",
    "clickhouse-driver",
    "numpy",
    "pandas",
    "sqlalchemy",
    "pymysql",
    "azure-cognitiveservices-speech",
```

单元测试:
```bash
pytest
```

### 1. db utils
- [x] mysql
```python
# mysql配置
mysql_config = {
  "host": "xxx"
  "port": xxx
  "user" : "xxx"
  "password" :"xxx"
  "database" : "xxx"
}

mysql_op = MysqlOperator(**mysql_config)

# 接口1: 获取所有表名
tables: set[str] = mysql_op.fetch_all_tables()

# 接口2: 执行`查询sql`,返回执行结果
data: DataFrame, columns: list[str] = mysql_op.fetch_specify_sql_data("SELECT * FROM customers")

# 接口3: 执行`插入sql`，使用指定dataframe数据，指定表名
need_insert_data = [
    {"customer_name": "test1", "email": "test1@gmail.com"},
    {"customer_name": "test2", "email": "test2@gmail.com"},
]
need_insert_dataframe = pd.DataFrame(need_insert_data)
rows: int = mysql_op.insert_database_mysql(need_insert_dataframe, "customers")
```
### 2. file storage
- [x] local storage
```python
# 接口对象
local_config = {
  "storage_home_dir" = "xxx"
}
local = LocalStorage(**local_config)

# 接口1: 写入本地文件内容
file_name: str = "test_save_file.txt"
content: bytes = "abc测试123!@!@".encode()

# file_path 是路径
status: bool, file_path: str = local_obj.save(file_name, content)

# 接口2: 读取本地文件内容
file_name: str = "test_save_file.txt"
content: bytes = "abc测试123!@!@".encode()

status: bool, actual_content: str = local_obj.load(file_name)
```
- [x] tencent cos storage
```python
# 接口对象
tencent_cos_config = {
    "bucket": "xxx",
    "region": "xxx",
    "secret_key": "xxx",
    "secret_id": "xxx"
}
tencent_cos = TencentCos(**tencent_cos_config)

# 接口1: 写入cos文件内容
file_name: str = "test_save_file.txt"
content: bytes = "abc测试123!@!@".encode()

status: bool, actual_file_name: str = tencent_cos_obj.save(
    filename=file_name, content=content
)

# 接口2: 读取cos文件内容
file_name: str = "test_save_file.txt"

status: bool, actual_content: bytes = tencent_cos_obj.load(file_name)
```
### 3. translation
> 封装翻译接口
>

- [x] mircrosoft 翻译
```python
from common_packages.translate import SentenceInfo, WordInfo
from common_packages.translate.microsoft import TranslateMicrosoft

# -------  初始化 -------
config: dict = {
  "text_endpoint": "xxx",
  "word_endpoint": "xxx",
  "word_sample_endpoint": "xxx",
  "location_region": "xxx",
  "key": "xxx",
  "tts_microsoft_config": {
    "key": "xxx",
    "location_region": "xxx",
}
microsoft_obj = TranslateMicrosoft(**config)

# ------- 1. 单词api -------
# 获取原生单词翻译结果
raw_word_translate_res = translate_microsoft_obj.translate_word(
    word="fly",
    source_language_code="en",
    target_language_code="zh-CN",
)
# 格式化为标准结果
res: WordInfo = translate_microsoft_obj.format_word_response(raw_word_translate_res)


# ------- 2. 句子api -------
# 获取原生句子翻译结果
res_tran: dict = translate_microsoft_obj.translate_sentence(
    text=self.text,
    source_language_code=self.source_language_code,
    target_language_code=self.target_language_code,
)
# 格式化为标准结果
res: SentenceInfo = translate_microsoft_obj.format_sentence_response(sentence_translate_data)
```
- 参考：
  - []()
    - 创建文本翻译服务
  - [tts文档](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/index-text-to-speech)
    - 创建tts服务：在`Azure` --> `Azure AI services` --> `语音服务`

- 将要支持的:
  - [ ] google 翻译
  - [ ] Deepl 翻译
  - [ ] openAI 翻译
- 不打算支持的:
  - tencent 翻译,翻译质量较差
  - youdao 翻译

### 3. Ai接口
> 解释句子,分析长难句
- [ ] openAI 翻译
- [ ] gemini 翻译

### 4. sms
腾讯云
```python

```

- [x] 可选导入模块,未安装时,提示安装!

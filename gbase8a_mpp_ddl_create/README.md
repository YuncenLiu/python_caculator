

执行前 删除 .DS_Sotre 文件避免 datax 执行失败
```shell
cd /Users/xiang/xiang/compile/datax

find ./ -name '.DS_Store' | xargs rm -f
```

执行 Python DataX
```shell
 python \
 /Users/xiang/xiang/compile/datax/bin/datax.py \
 /Users/xiang/xiang/study/Python/tools/caculator/target/gbase8a_source_json/xg/T02SELLQUALIFYINFO.json
```


```shell
 python \
 /Users/xiang/xiang/compile/datax/bin/datax.py \
 /Users/xiang/xiang/study/Python/tools/caculator/target/gbase8a_target_json/xg/T02SELLQUALIFYINFO.json
```
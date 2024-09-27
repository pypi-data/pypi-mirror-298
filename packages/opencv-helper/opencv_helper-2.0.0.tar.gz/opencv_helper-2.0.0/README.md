### 生成包

```python
python3 setup.py sdist bdist_wheel
```

发布

```shell
pip install twine

twine upload dist/\*
```

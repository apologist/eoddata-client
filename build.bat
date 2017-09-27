@echo off
echo Building package...

rmdir /Q /S dist
rmdir /Q /S build	
rmdir /Q /S eoddata_client.egg-info

python setup.py bdist_wheel

echo Publishing package...
twine upload --config-file .pypirc dist\*

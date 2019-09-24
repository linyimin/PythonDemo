@echo off
set CLASSPATH=%CLASSPATH%;  
set PATH=%PATH%  
set JAVA_HOME=%JAVA_HOME%

java -jar swagger-codegen-cli.jar generate -i swagger.json -o cpprest-clientnt -l cpprest


@echo off

echo :::::: Cyclomatic Complexity: ::::::
echo presione una tecla para calcular
pause > nul

radon cc -i tests -a -s . 
radon cc -i tests -a -s . > metrics/cyclomatic_complexity.txt


echo :::::: Maintainability Index: ::::::
echo presione una tecla para calcular
pause > nul

radon mi -s -m .
radon mi -s -m . > metrics/maintainability_index.txt


echo :::::: Raw Metrics ::::::
echo presione una tecla para calcular
pause > nul

radon raw -s .
radon raw -s . > metrics/raw_metrics.txt


echo :::::: Halstead Metrics ::::::
echo presione una tecla para calcular
pause > nul

radon hal -e "*__init__.py" app
radon hal -e "*__init__.py" app > metrics/halstead_metrics.txt
echo :::::: FINISH ::::::
echo presione una tecla para salir
pause > nul
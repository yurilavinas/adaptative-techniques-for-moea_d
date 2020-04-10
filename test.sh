# Usage
# python MOEAD.py [parameter yml file] [random seed]
 
for i in {1000..1001} ; do
    python AMOEAD.py config.yml ${i}
done

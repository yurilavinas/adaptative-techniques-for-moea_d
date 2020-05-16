for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_adaptive/DTLZ1_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_adaptive/DTLZ2_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_adaptive/DTLZ3_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_adaptive/DTLZ4_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_adaptive/DTLZ5_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_adaptive/DTLZ6_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_adaptive/DTLZ7_adaptive.yml ${i}
done

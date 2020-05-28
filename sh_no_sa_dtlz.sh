for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_no_sa/DTLZ1_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_no_sa/DTLZ2_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_no_sa/DTLZ3_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_no_sa/DTLZ4_adaptive.yml ${i}
done

for i in {0..10} ; do
    python3 AMOEAD.py exp_scripts_no_sa/DTLZ5_adaptive.yml ${i}
done

for i in {0..10} ; do
   python3 AMOEAD.py exp_scripts_no_sa/DTLZ6_adaptive.yml ${i}
done

 for i in {0..10} ; do
     python3 AMOEAD.py exp_scripts_no_sa/DTLZ7_adaptive.yml ${i}
 done

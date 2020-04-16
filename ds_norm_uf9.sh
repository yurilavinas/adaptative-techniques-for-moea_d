 s# Usage
# python MOEAD.py [parameter yml file] [ds_norm seed]
 
for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_1.yml ${i} & 
    pids[${i}]=$!
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_2ml ${i} &
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_3.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_4.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_5.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_6.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_7.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_8.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_148.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_48.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_28.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_248.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done

for i in {0..10} ; do
    nohup python3 MOEAD_collab.py exp_scripts/ds_norm_uf9/ds_solutions_98.yml ${i}
done
for pid in ${pids[*]}; do
    wait $pid
done
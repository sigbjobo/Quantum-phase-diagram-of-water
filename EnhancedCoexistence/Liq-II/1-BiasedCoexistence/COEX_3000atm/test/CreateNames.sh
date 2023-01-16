
echo $1 $2
rm names.pdb
if [ $1 -eq 0 ]
then
    for i in $(seq 1 $2)
    do
	let O1=($i-1)*3+1
	let H1=($i-1)*3+2
	let H2=($i-1)*3+3
	echo ATOM      $O1  O       X   $i       0.000   2.593   4.126  0.00  0.00           O>> names.pdb
    done
    for i in $(seq 1 $2)
    do
	let O1=($i-1)*3+1
	let H1=($i-1)*3+2
	let H2=($i-1)*3+3
	echo ATOM      $O1  O       X   $i       0.000   2.593   4.126  0.00  0.00           O>> names.pdb
	echo ATOM      $H1  H       X   $i       0.000   3.509   3.847  0.00  0.00           H>> names.pdb
	echo ATOM      $H2  H       X   $i       0.000   2.635   5.083  0.00  0.00           H>> names.pdb
    done
    
else
    for i in $(seq 1 $2)
    do
	let O1=($i-1)*3+1
	let H1=($i-1)*3+2
	let H2=($i-1)*3+3
	echo ATOM      $O1  O       X   $i       0.000   2.593   4.126  0.00  0.00           O>> names.pdb
	echo ATOM      $H1  H       X   $i       0.000   3.509   3.847  0.00  0.00           H>> names.pdb
	echo ATOM      $H2  H       X   $i       0.000   2.635   5.083  0.00  0.00           H>> names.pdb
    done
fi

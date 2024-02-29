rama_origen=$(git rev-parse --abbrev-ref HEAD)

git checkout book_branch
error=$?
if ! [ $error == 0 ] ; then
    exit
fi

git reset --hard $rama_origen
error=$?
if ! [ $error == 0 ] ; then
    exit
fi

./Notebook_to_myst.sh
error=$?
if ! [ $error == 0 ] ; then
    exit
fi

git add ../
error=$?
if ! [ $error == 0 ] ; then
    exit
fi

git commit -m "Compilamos book"
error=$?
if ! [ $error == 0 ] ; then
    exit
fi

git push origin book_branch
error=$?
if ! [ $error == 0 ] ; then
    exit
fi

git checkout $rama_origen
error=$?
if ! [ $error == 0 ] ; then
    exit
fi

rama_origen=$(git rev-parse --abbrev-ref HEAD)

git diff --quiet
error=$?
if ! [ $error == 0 ] ; then
    echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`
    exit
fi


git checkout book_branch
error=$?
if ! [ $error == 0 ] ; then
    echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`
    exit
fi

git reset --hard $rama_origen
error=$?
if ! [ $error == 0 ] ; then
    echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`
    exit
fi

./Notebook_to_myst.sh
error=$?
if ! [ $error == 0 ] ; then
    echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`
    exit
fi

git add ../
error=$?
if ! [ $error == 0 ] ; then
    echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`
    exit
fi

git commit -m "Compilamos book"
error=$?
if ! [ $error == 0 ] ; then
    echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`
    exit
fi

git pull -s recursive -X ours origin book_branck
error=$?
if ! [ $error == 0 ] ; then
    echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`
    exit
fi


git push origin book_branch
error=$?
if ! [ $error == 0 ] ; then
    echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`
    exit
fi

git checkout $rama_origen
error=$?
if ! [ $error == 0 ] ; then
    echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`
    exit
fi

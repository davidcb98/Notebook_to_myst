rama_origen=$(git rev-parse --abbrev-ref HEAD)

git checkout book_branch
git reset --hard $rama_origen
./Notebook_to_myst.sh
git add ../
git commit -m "Compilamos book"
git push origin book_branch
git checkout $rama_origen

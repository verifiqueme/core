pipenv install --system
find / -iname '*.cpp' -exec echo sed -i 's/locale\.h/locale2.h/g' '{}' ';'

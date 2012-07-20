
###TODO
# (complete)디렉토리에는 RCS 디렉토리가 포함되어 있다. RCS를 빼고 zip 하도록 하자.


###Logs

#0908191432 bug fix: zip가 aaa/ directory를 zip 할 때에 디렉토리를 그대로 zip
#해버렸다. 즉 zip 파일에는 aaa/FILE 이런식으로 내용이 존재한다. 이것을 xpi로
#바꾸어 설치를 하면 firefox는 install file을 찾을 수 없다는 메세지를 알려준다.
#이 문제를 해결





DIR=oswk

FILENAME=oswk
FILENAMEZIP=oswk.zip
FILENAMEXPI=oswk.xpi
FILENAMEXPIBAK=oswk.xpi.bak

# Backup xpi file
if [ -f $FILENAMEXPI ]; then
    echo "Rename" $FILENAMEXPI "to" $FILENAMEXPIBAK
    mv $FILENAMEXPI $FILENAMEXPIBAK
    fi

# There is only oswk.xpi.bak file

echo "Move" $DIR
cd $DIR

# The version control files and backup file have no need to archive.
zip -r $FILENAME ./ -x "RCS/" -x "*/RCS/*" -x "*~"

echo "Rename" $FILENAMEZIP "to" $FILENAMEXPI
mv $FILENAMEZIP ../$FILENAMEXPI

cd ../


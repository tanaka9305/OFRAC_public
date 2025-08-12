Race Studio 2で出力したCSVはShift-JISでエンコードされているみたいです．
CSVを読み込む際に文字コードを指定しないといけないといけないので，このコード
内ではShift-JISで指定しています．

しかしExcelなどCSV出力するとUTF-8になってしまうので，読み込めなくなります．
その場合は，コード内25行目あたり

encoding = 'shift_jis'

を
encoding = 'utf_8'

に変えてください．

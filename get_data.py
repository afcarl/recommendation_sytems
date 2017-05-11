import csv
import os.path
import numpy as np
import scipy.sparse as sp

data_link = 'http://www2.informatik.uni-freiburg.de/~cziegler/BX/BX-CSV-Dump.zip'
data_path = 'data/'
book_num = -1

def file_not_found():
    print('Data File Not Found')
    print('Download the data from the link below (~25Mb). Extract and paste its contents in data folder in the project folder')
    print('         %s' %link)

def download_data():
    print('Downloading...')
    # to_do: Write Download method

def parse(data):
    csv_data = csv.reader(data, delimiter=';')

    for row in csv_data:
        # print(row)
        uid, isbn, rating,book_id = row


        # Subtract one from ids to shift
        # to zero-based indexing
        yield int(uid) - 1, isbn , rating,book_id

def get_dimensions(train_data):
    uids = set()
    book_ids = set()

    for uid, _, _,book_id in train_data:
        if not book_id == '?':
            uids.add(uid)
            book_ids.add(int(book_id))

    row = max(uids) + 1
    col = max(book_ids) + 1

    return row,col

def convert_book_data(data):
    ctr = 0
    list_of_books = []

    csv_file = csv.reader(data,delimiter=';')
    next(csv_file)
    with open(data_path + 'books.csv','w') as converted_book_data:
        w_csv_file = csv.writer(converted_book_data,delimiter=';')
        for row in csv_file:
            w_csv_file.writerow([ctr] + row[:3])
            list_of_books.append([ctr] + row[:3])
            # print([ctr] + row[:4])
            ctr += 1

def convert_main_data(data,books):
    csv_file = csv.reader(data,delimiter=';')
    next(csv_file)
    with open(data_path + 'rating.csv','w') as converted_rating_data:
        w_csv_file = csv.writer(converted_rating_data,delimiter=';')
        for row in csv_file:
            try:
                w_csv_file.writerow(row + [books[row[1]]])
                # print(row + [str(books[row[1]])])
            except KeyError:
                w_csv_file.writerow(row + ['?'])
                # print(row + ['?'])



def make_array():
    ctr = 0
    list_of_books = []
    dict_of_books = {}
    with open(data_path + 'books.csv',errors='backslashreplace') as fi:
        csv_file = csv.reader(fi,delimiter=';')
        for row in csv_file:
            # print(row[0])
            list_of_books.append(row)
            dict_of_books[row[1]] = ctr
            ctr += 1
    return list_of_books,dict_of_books


def build_matrix(rows, cols, data, min_rating):
    mat = sp.lil_matrix((rows, cols), dtype=np.int32)

    for uid, _, rating, book_id in data:
        if rating >= min_rating:
            mat[uid, book_id] = rating

    return mat.tocoo()



def fetch_bx_book_ratings(min_rating = 0,download_if_missing = True):

    if not os.path.isfile(data_path + 'rating.csv') or not os.path.isfile(data_path + 'books.csv') :
        print('HELLO')
        try:
            main_data = open(data_path + 'BX-Book-Ratings.csv',errors='backslashreplace')
            books = open(data_path + 'BX-Books.csv',errors='backslashreplace')
            users = open(data_path + 'BX-Users.csv',errors='backslashreplace')
        except FileNotFoundError:
            if download_if_missing == False:
                file_not_found()
            else:
                dowload_data()

        if not os.path.isfile(data_path + 'books.csv'):
            convert_book_data(books)

        list_of_books,dict_of_books = make_array()

        assert list_of_books[10][0] == '10'
        assert list_of_books[27138][0] == '27138'
        assert dict_of_books['0671870432'] == 7
        assert dict_of_books['0231128444'] == 271367

        if not os.path.isfile(data_path + 'rating.csv'):
            convert_main_data(main_data,dict_of_books)

        books.close()
        main_data.close()
        users.close()

    else:
        list_of_books,dict_of_books = make_array()
        with open(data_path + 'rating.csv') as main_file:
            row,col = get_dimensions(parse(main_file))
            # print(row,col)
            train = build_matrix(row,col,parse(main_file),min_rating)
            # print('TRAIN DATA')
            # print(train.shape)

    assert list_of_books[10][0] == '10'
    assert list_of_books[27138][0] == '27138'
    assert dict_of_books['0671870432'] == 7
    assert dict_of_books['0231128444'] == 271367

    return {
    'train' : train,
    'list_of_books' : list_of_books,
    'dict_of_books': dict_of_books
    }






        # row, col = get_dimension(parse(main_data))

def main():
    a = fetch_bx_book_ratings(min_rating = 8)


if __name__ == '__main__':
    main()

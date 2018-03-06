# coding: utf-8

import os
import warnings

import pandas as pd
from sklearn.exceptions import DataConversionWarning

import dataprep
import tokenizing

warnings.filterwarnings(action='ignore', category=DataConversionWarning)

DATADIR = os.getenv('DATADIR')

if __name__ == "__main__":
    new_content = pd.read_csv(
        os.path.join(DATADIR, 'new_content.csv.gz'),
        dtype=object,
        compression='gzip'
    )

    new_content.drop(['content_purpose_document_supertype', 'content_purpose_subgroup',
                      'content_purpose_supergroup', 'email_document_supertype',
                      'government_document_supertype', 'navigation_document_supertype',
                      'public_updated_at', 'search_user_need_document_supertype',
                      'taxon_id', 'taxons', 'user_journey_document_supertype', 'updated_at'], axis=1, inplace=True)

    # **** VECTORIZE META ********************
    # ************************************

    print("Vectorizing metadata")
    meta = dataprep.create_meta(new_content['content_id'], new_content)

    # **** TOKENIZE TEXT ********************
    # ************************************

    # Load tokenizers, fitted on both labelled and unlabelled data from file
    # created in clean_content.py

    print("Tokenizing combined_text")

    combined_text_sequences_padded = dataprep.create_padded_combined_text_sequences(
        new_content['combined_text'])

    # prepare title and description matrices,
    # which are one-hot encoded for the 10,000 most common words
    # to be fed in after the flatten layer (through fully connected layers)

    print('one-hot encoding title sequences')

    title_onehot = dataprep.create_one_hot_matrix_for_column(
        tokenizing.load_tokenizer_from_file(
            os.path.join(DATADIR, "title_tokenizer.json")
        ),
        new_content['title'],
        num_words=10000,
    )

    print('title_onehot shape {}'.format(title_onehot.shape))

    print('one-hot encoding description sequences')

    description_onehot = dataprep.create_one_hot_matrix_for_column(
        tokenizing.load_tokenizer_from_file(
            os.path.join(DATADIR, "description_tokenizer.json")
        ),
        new_content['description'],
        num_words=10000,
    )

    print('description_onehot shape {}'.format(description_onehot.shape))

    print('producing arrays for new_content')

    data = {
        "x": combined_text_sequences_padded,
        "meta": meta,
        "title": title_onehot,
        "desc": description_onehot,
        "content_id": new_content['content_id']
    }

    dataprep.process_split('predict', (0, new_content.shape[0]), data)

    print("Finished")

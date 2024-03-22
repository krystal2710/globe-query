from datasets import load_dataset

if __name__=="__main__":
    docpairs = load_dataset('irds/msmarco-passage_train_triples-small', 'docpairs')
    i=0
    for record in docpairs:
        if i == 10:
            break
        print(record)
        i+=1
    print(type(docpairs))
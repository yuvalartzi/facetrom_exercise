import vector

if __name__ == '__main__':
    vector.create_facial_vectors()
    vector.calc_mean_and_std()
    res = vector.get_exceptional_images()

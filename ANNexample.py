import numpy as np
from annoy import AnnoyIndex

# Function to generate random track embeddings (replace this with your actual data loading code)
def generate_random_embeddings(num_tracks, embedding_dim):
    return [np.random.rand(embedding_dim) for _ in range(num_tracks)]

# Function to build the Annoy index in chunks
def build_ann_index_in_chunks(track_embeddings, chunk_size=4000, num_trees=100):
    embedding_dim = len(track_embeddings[0])
    num_tracks = len(track_embeddings)
    annoy_index = AnnoyIndex(embedding_dim, 'angular')  # Angular distance is suitable for cosine similarity

    # Build the index in chunks
    for i in range(0, num_tracks, chunk_size):
        chunk_end = min(i + chunk_size, num_tracks)
        for j, embedding in enumerate(track_embeddings[i:chunk_end]):
            annoy_index.add_item(i + j, embedding)
        print("Built index for chunk {} to {}".format(i, chunk_end))
    print("\n\n")
    annoy_index.build(num_trees)
    return annoy_index

# Function to save the Annoy index to disk
def save_ann_index(ann_index, index_filename):
    ann_index.save(index_filename)

# Function to load the Annoy index from disk
def load_ann_index(index_filename, embedding_dim):
    ann_index = AnnoyIndex(embedding_dim, 'angular')
    ann_index.load(index_filename)
    return ann_index

# Function to perform nearest neighbor search using the Annoy index
def find_nearest_neighbors(ann_index, track_id, num_neighbors=5):
    nearest_neighbor_ids = ann_index.get_nns_by_item(track_id, num_neighbors)
    return nearest_neighbor_ids

if __name__ == "__main__":
    # Generate random track embeddings (replace this with your actual data loading code)
    num_tracks = 106574  # Number of tracks
    embedding_dim = 128  # Dimensionality of track embeddings
    track_embeddings = generate_random_embeddings(num_tracks, embedding_dim)

    # Build Annoy index in chunks
    ann_index = build_ann_index_in_chunks(track_embeddings, chunk_size=10000, num_trees=100)

    # Save Annoy index to disk
    index_filename = 'track_annoy_index.ann'
    save_ann_index(ann_index, index_filename)

    # Later, you can load the index from disk
    ann_index_loaded = load_ann_index(index_filename, embedding_dim)

    # Prompt the user to input a track ID
    while True:
        try:
            track_id = int(input("Enter a track ID (0 to {}): ".format(num_tracks - 1)))
            if track_id < 0 or track_id >= num_tracks:
                raise ValueError("Track ID must be between 0 and {}".format(num_tracks - 1))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    # Perform nearest neighbor search for the input track ID
    num_neighbors = 20
    nearest_neighbor_ids = find_nearest_neighbors(ann_index_loaded, track_id, num_neighbors)
    print("Nearest neighbor IDs of track {}: {}".format(track_id, nearest_neighbor_ids))


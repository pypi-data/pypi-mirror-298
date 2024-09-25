import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def rgb2gray(image):
    """
    將 RGB 圖像轉換為灰階圖像。
    """
    return np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])

def svd_compress(image_matrix, k):
    """
    使用奇異值分解（SVD）來壓縮圖像。
    
    參數:
    image_matrix: 以 2D numpy 陣列形式表示的灰階圖像。
    k: 保留的奇異值數量，用於壓縮。
    
    返回:
    compressed_image: 使用前 k 個奇異值重建的壓縮圖像。
    """
    U, S, Vt = np.linalg.svd(image_matrix, full_matrices=False)
    compressed_image = np.dot(U[:, :k], np.dot(np.diag(S[:k]), Vt[:k, :]))
    
    return compressed_image

def plot_compressed_images(gray_image, k_values):
    """
    同時顯示不同 k 值下壓縮的圖像。
    
    參數:
    gray_image: 灰階圖像矩陣。
    k_values: 奇異值的取值列表。
    """
    fig, axes = plt.subplots(1, len(k_values), figsize=(15, 6))

    for i, k in enumerate(k_values):
        compressed_image = svd_compress(gray_image, k)
        axes[i].imshow(compressed_image, cmap='gray')
        axes[i].set_title(f'k={k}')
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

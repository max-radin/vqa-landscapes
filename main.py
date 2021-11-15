import argparse
import pyqtgraph as pg
from app import create_landscape_app
from compute_landscape import compute_landscape

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--save-images",
        action="store_true",
        default=False,
        help="Whether to save images for each frame.",
    )
    parser.add_argument(
        "-n-steps",
        type=int,
        default=100,
        help="Number of steps to use along each dimension. Use smaller values for faster scans.",
    )

    args = parser.parse_args()
    parameter_trajectory, losses, pca, scan_pca_result = compute_landscape(
        n_steps=args.n_steps
    )
    create_landscape_app(
        parameter_trajectory=parameter_trajectory,
        losses=losses,
        pca=pca,
        scan_pca_result=scan_pca_result,
        save_images=args.save_images,
    )

    pg.exec()

from setuptools import setup
from mlx import extension

if __name__ == "__main__":
    setup(
        name="mlx_cluster",
        version="0.0.3",
        description="Sample C++ and Metal extensions for MLX primitives.",
        ext_modules=[extension.CMakeExtension("mlx_cluster._ext")],
        cmdclass={"build_ext": extension.CMakeBuild},
        packages=["mlx_cluster"],
        package_data={"mlx_cluster": ["*.so", "*.dylib", "*.metallib"]},
        extras_require={
            "dev": [],
            "test": [
                "mlx_graphs",
                "torch",
                "pytest",
            ],
        },
        zip_safe=False,
        python_requires=">=3.8",
    )

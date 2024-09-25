import os


def main():
    # Get the absolute path to the app.py file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, 'app.py')

    # Run the Streamlit app using the absolute path
    os.system(f'streamlit run {app_path}')


if __name__ == '__main__':
    main()
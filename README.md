# Zenerator
### *Generate haikus from text or code with Zenerator, your poetic companion.*

This is a haiku generator that generates haikus based on the provided input text. It can generate haikus from any given text or code from a GitHub repository.

## Features

Generate haikus from any text input
Option to generate haikus from code in a GitHub repository
RESTful API endpoint to generate haikus
Display the generated haiku using a template
Simple and easy-to-use interface

## Prerequisites

Python 3.6 or above installed
Required Python packages installed (see requirements.txt)

## API Endpoint

The haiku generator provides a RESTful API endpoint to generate haikus. Send a POST request to /haiku with the following parameters:  
  **text** *(required)*: The input text or code.  
  **is_code** *(optional)*: Set to true if the input is code from a GitHub repository.  
The API will respond with a JSON object containing the generated haiku.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the haiku generator, please feel free to submit a pull request.

## Acknowledgements

This haiku generator is inspired by the beauty of haiku poetry.
The code-fetching functionality is based on the GitHub API.

## Contact

For any inquiries or suggestions, please contact fotios.pechlivanis@gmail.com.

Enjoy creating beautiful haikus!

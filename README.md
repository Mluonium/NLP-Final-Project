
# NLP exam project

Exploring the impact of language similarity on fine-tuned mBERT models for under-resourced languages


## Authors

- [@Mluonuim](https://github.com/Mluonium)
- [@JosefineNyeng](https://github.com/JosefineNyeng)
- [@AnnaMariaGnat](https://github.com/AnnaMariaGnat)

## Hugging Face token 

To run parts of the code, it may be necessary to paste in a Hugging face token, which you can get from here, after logging in: https://huggingface.co/settings/tokens.
## File guide

The 00_running_models_on_test_data.ipynb file was made to run a model on all the test languages at once and output a file with the predictions for each language. Within the file specify the model_language at the top to indicate which model to test. Lastly, within the data folder we have a file called 01_testing_span_f1.ipynb which computes the span f1 of a model's predictions compared to the gold-standard labels. Again within this file model_langugae at the top specifies which model to compute the span-f1 for.
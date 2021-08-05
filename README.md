# Cowin notifier
Vaccine notifier using cowin public api and python.

# local setup

```sh
git clone https://github.com/gurusabarish/cowin-notifier.git
cd cowin-notifier
pip install -r requirements.txt
```

# Run on your machine
**Fill your email detail in .env file**

```python
python manage.py createsuperuser
python manage.py runserver localhost:8080
```
- Go to  [localhost:8080/states-and-districts](http://localhost:8080/states-and-districts) to featch the state and district details
- Now, Go to [localhost:8080](http://localhost:8080) and register
- After that, run the main script by entering http://localhost:8080/runscript on browser


## Issues

If you have a question, please [open an issue](https://github.com/gurusabarish/cowin-notifier/issues) for help and to help those who come after you. The more information you can provide, the better!

## Contributing

Contributions, issues, and feature requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

Licensed under [MIT](LICENSE)

## 🤝 Support

Give a ⭐️ if you like this project!

<a href="https://www.buymeacoffee.com/gurusabarish" target="_blank" rel="noopener"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="40" width="145" alt="Buy Me A Coffee"></a>

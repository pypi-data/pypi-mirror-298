This package allows users to access the Water Stable Isotope Database in Peru. Provides an interactive map for exploring the spatial distribution of all the stations. Additionally, it offers features for technical validation and display temporal series for each station and department across Peru. For more information, users can refer to the package [GitHub](https://github.com/karoru23/WSI-PeruDB) page.

Users must install JupyterLab or Jupyter Notebook. Additionally, users must use the **Chrome Browser** to visualize the interface 

# Usage 

```python
import WSIPeruDB
```
## Display the spatial distribution of stable isotope stations.
```
WSIPeruDB.generate_map()
```
## Get station information. In this section, users will be able to see whether the station data is located in the WSIPeruDB or in another repository, along with the respective Project_ID assigned in that repository to facilitate the search.
```
WSIPeruDB.department_information()
```
## Plot Linear Meteoric Water Line (LMWL)
```
WSIPeruDB.plot_lmwl()
```
## Display temporal series and histogram 
```
WSIPeruDB.analyze_temporal_series()
```
## Comparing dataset departments
```
WSIPeruDB.compare_departments()
```
## Download dataset information
```
WSIPeruDB.download_dataset()
```
## Download site information 
```
WSIPeruDB.download_site_information()
```

# Add or Download Data from WSIPeruDB package

Users must fill the request through this [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSfikgyxrKKnKIHRzj7CgmXvYh3pv7Psu4D5wsl4ps1ZCZQCmw/viewform?vc=0&c=0&w=1&flr=0) either for add or download data from the WSI-PeruDB. This is necessary for us to maintain statistics about the database. 

# License

[MIT](https://choosealicense.com/licenses/mit/)
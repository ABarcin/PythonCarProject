using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using PythonCarProject.UI.Models;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace PythonCarProject.UI.Controllers
{
    public class CarController : Controller
    {
        static HttpClient client = new HttpClient();
        public IActionResult Index()
        {
            return View();
        }
        [HttpPost]
        public async Task<IActionResult> GetCars(Car car)
        {
            HttpResponseMessage response;
            string responseBody;
            client.Timeout = TimeSpan.FromSeconds(600);
            List<Car> Cars = new List<Car>();
            if (car.Brand == null && car.Color == null && car.Year == null && car.Transmission == null)
            {
                client.BaseAddress = new Uri("http://127.0.0.1:5000");
                response = await client.GetAsync("http://127.0.0.1:5000/cars/list");
                response.EnsureSuccessStatusCode();
                responseBody = await response.Content.ReadAsStringAsync();
                var obj = JsonConvert.DeserializeObject<dynamic>(responseBody);
                foreach (var item in obj)
                {
                   // price,brand,color,trans,year,img
                    Car temp = new Car()
                    {
                        Title=item[0],
                        Price=item[1],
                        Brand=item[2],
                        Color=item[3],
                        Transmission=item[4],
                        Year=item[5],
                        ImagePath=item[6]
                    };
                    Cars.Add(temp);
                }
            }
            else
            {
                client.BaseAddress = new Uri("http://127.0.0.1:5000");
                #region SetUrlForFilters
                string url = "";
                if (car.Brand != null)
                {
                    url += "brand=" + car.Brand.ToLower();
                }
                if (car.Color != null && url == null)
                {
                    url += "extcolor=" + car.Color.ToLower();
                }
                else if (car.Color != null)
                {
                    url += "&extcolor=" + car.Color.ToLower();
                }
                if (car.Year != null && url == null)
                {
                    url += "year=" + car.Year;
                }
                else if (car.Year != null)
                {
                    url += "&year=" + car.Year;
                }
                if (car.Transmission != null && url == null)
                {
                    url += "trans=" + car.Transmission.ToLower();
                }
                else if (car.Transmission != null)
                {
                    url += "&trans=" + car.Transmission.ToLower();
                } 
                #endregion
                response = await client.GetAsync("http://127.0.0.1:5000/cars/list?"+url);
                response.EnsureSuccessStatusCode();
                responseBody = await response.Content.ReadAsStringAsync();
                var obj = JsonConvert.DeserializeObject<dynamic>(responseBody);
                foreach (var item in obj)
                {
                    // price,brand,color,trans,year,img
                    Car temp = new Car()
                    {
                        Title = item[0],
                        Price = item[1],
                        Brand = item[2],
                        Color = item[3],
                        Transmission = item[4],
                        Year = item[5],
                        ImagePath = item[6]
                    };
                    Cars.Add(temp);
                }
            }

            return View(Cars);
        }
    }
}

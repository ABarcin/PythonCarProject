using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Newtonsoft.Json;
using PythonCarProject.UI.Common;
using PythonCarProject.UI.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace PythonCarProject.UI.Controllers
{
    public class CarController : Controller
    {
        public async Task<IActionResult> Index()
        {
            HttpClient client = new HttpClient();
            HttpResponseMessage response;
            if (Filters.Brands==null)
            {
                Filters.Brands = new List<SelectListItem>();
                Filters.Colors = new List<SelectListItem>();
                Filters.Trans = new List<SelectListItem>();
                Filters.Years = new List<SelectListItem>();
            }
            string responseBody;
            client.BaseAddress = new Uri("http://127.0.0.1:5000");
            response = await client.GetAsync("cars/filters");
            response.EnsureSuccessStatusCode();
            responseBody = await response.Content.ReadAsStringAsync();
            var obj = JsonConvert.DeserializeObject<List<string>>(responseBody);
            int count = 0;
            foreach (var item in obj)
            {
                if (item!="")
                {
                    if (item== "nextfilter")
                    {
                        count++;
                    }
                    else
                    {
                        if (count == 0)
                        {
                            Filters.Brands.Add(new SelectListItem() { Text = item.ToUpper(), Value = item.ToLower() });
                        }
                        if (count == 1)
                        {
                            Filters.Colors.Add(new SelectListItem() { Text = item.ToUpper(), Value = item.ToLower() });
                        }
                        if (count == 2)
                        {
                            Filters.Trans.Add(new SelectListItem() { Text = item.ToUpper(), Value = item.ToLower() });
                        }
                        if (count == 3)
                        {
                            Filters.Years.Add(new SelectListItem() { Text = item.ToUpper(), Value = item.ToLower() });
                        }
                    }
                    
                }
            }
            ViewBag.brand = Filters.Brands.ToList(); ViewBag.color = Filters.Colors.ToList(); ViewBag.tran = Filters.Colors.ToList(); ViewBag.year = Filters.Years.ToList();
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> GetCars(Car car)
        {
            HttpClient client = new HttpClient();
            client.DefaultRequestHeaders.Accept.Clear();
            HttpResponseMessage response;
            client.BaseAddress = new Uri("http://127.0.0.1:5000");
            string responseBody;
            ViewBag.brand = Filters.Brands.ToList(); ViewBag.color = Filters.Colors.ToList(); ViewBag.tran = Filters.Colors.ToList(); ViewBag.year = Filters.Years.ToList();
            client.Timeout = TimeSpan.FromSeconds(600);
            List<Car> Cars = new List<Car>();
            if (car.Brand == null && car.Color == null && car.Year == null && car.Transmission == null)
            {
                response = await client.GetAsync("cars/list");
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
                response = await client.GetAsync("cars/list?"+url);
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

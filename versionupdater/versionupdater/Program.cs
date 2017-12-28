using CommandLine;
using Csv;
using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Text.RegularExpressions;

namespace versionupdater
{
    class Program
    {
        static void Main(string[] args)
        {
            Parser.Default.ParseArguments<CommandLineOptions>(args).WithParsed(async options =>
            {
                if (!string.IsNullOrWhiteSpace(options.CsvPath))
                {
                    StringBuilder builder = new StringBuilder();
                    using (FileStream stream = new FileStream(options.CsvPath, FileMode.Open))
                    {
                        CsvOptions csvOptions = new CsvOptions();
                        csvOptions.HeaderMode = HeaderMode.HeaderAbsent;

                        var csvFile = CsvReader.ReadFromStream(stream, csvOptions);
                        foreach(var line in csvFile)
                        {
                            var packageId = line[1];
                            packageId = Regex.Replace(packageId, @"(\[(.*?)\])*", "");

                            HttpClient client = new HttpClient();
                            var response = await client.GetAsync($"https://api.nuget.org/v3-flatcontainer/{packageId}/index.json");
                            var contents = await response.Content.ReadAsStringAsync();

                            JObject jsonContent = JObject.Parse(contents);
                            string version = jsonContent.First.First.Last.ToString();

                            Console.WriteLine(packageId);
                            Console.WriteLine("Latest version: " + version);

                            builder.AppendLine($"{line[0]},{line[1]},{version}");
                        }
                    }

                    File.WriteAllText(options.CsvPath, builder.ToString());
                }
            });

            Console.Read();
        }
    }
}

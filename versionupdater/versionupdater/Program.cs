using CommandLine;
using Csv;
using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace versionupdater
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Version Updater 1.0");
            if (args.Any())
            {
                foreach (string arg in args)
                {
                    Console.WriteLine(arg);
                }
            }

            Parser.Default.ParseArguments<CommandLineOptions>(args).WithParsed(options =>
            {
                if (!string.IsNullOrWhiteSpace(options.CsvPath))
                {
                    StringBuilder builder = new StringBuilder();
                    using (FileStream stream = new FileStream(options.CsvPath, FileMode.Open))
                    {
                        Console.WriteLine("File opened...");
                        CsvOptions csvOptions = new CsvOptions();
                        csvOptions.HeaderMode = HeaderMode.HeaderAbsent;

                        var csvFile = CsvReader.ReadFromStream(stream, csvOptions);

                        var csvLines = csvFile.ToList();
                        Console.WriteLine($"Lines in file: {csvLines.Count()}");

                        Task.Run(async () =>
                        {
                            foreach (var line in csvLines)
                            {
                                Console.WriteLine("Processing CSV entry...");

                                var packageId = line[1];
                                packageId = Regex.Replace(packageId, @"(\[(.*?)\])*", "");

                                Console.WriteLine($"Package ID: {packageId}");
                                HttpClient client = new HttpClient();
                                var response =
                                    await client.GetAsync(
                                        $"https://api.nuget.org/v3-flatcontainer/{packageId}/index.json");
                                var contents = await response.Content.ReadAsStringAsync();

                                JObject jsonContent = JObject.Parse(contents);
                                string version = jsonContent.First.First.Last.ToString();

                                Console.WriteLine(packageId);
                                Console.WriteLine("Latest version: " + version);

                                builder.AppendLine($"{line[0]},{line[1]},{version}");
                            }
                        }).Wait();
                    }

                    File.WriteAllText(options.CsvPath, builder.ToString());
                }
            });
        }
    }
}

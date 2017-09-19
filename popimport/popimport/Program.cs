using CommandLine;
using System;
using System.IO;
using System.Xml.Linq;

namespace popimport
{
    class Program
    {
        private const string FRAMEWORKS_FILE = "frameworks.xml";

        static void Main(string[] args)
        {
            ParserResult<CommandLineOptions> options = Parser.Default.ParseArguments<CommandLineOptions>(args);

            if (options != null)
            {
                options.WithParsed(t => ProcessData(t));
            }
        }

        static void ProcessData(CommandLineOptions options)
        {
            if (!string.IsNullOrWhiteSpace(options.FrameworksPath))
            {
                string text = Path.Combine(options.FrameworksPath, "frameworks.xml");
                if (File.Exists(text))
                {
                    XDocument xDocument = XDocument.Load(text);
                    foreach (XElement current in xDocument.Descendants("Frameworks").Descendants("Framework"))
                    {
                        string value = current.Attribute("Name").Value;
                        Console.WriteLine(string.Format("Operating on {0}", value));
                        string text2 = Path.Combine(options.FrameworksPath, value);
                        string[] files = Directory.GetFiles(text2, "*.xml");
                        for (int i = 0; i < files.Length; i++)
                        {
                            string path = files[i];
                            string fileNameWithoutExtension = Path.GetFileNameWithoutExtension(path);
                            if (File.Exists(Path.Combine(text2, fileNameWithoutExtension + ".dll")))
                            {
                                current.Add(new XElement("import", string.Format("{0}\\{1}", value, Path.GetFileName(path))));
                            }
                        }
                    }
                    xDocument.Save(text);
                    return;
                }
                Console.WriteLine("There was no frameworks.xml file found.");
            }
        }
    }
}

using System.IO.Compression;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        // specify the directory containing the zip files
        string directory = "path/to/directory";

        // loop through all files in the directory
        foreach (string filename in Directory.GetFiles(directory))
        {
            // check if the file is a zip file
            if (Path.GetExtension(filename).Equals(".zip", StringComparison.OrdinalIgnoreCase))
            {
                // create a ZipArchive object for the zip file
                using (ZipArchive archive = ZipFile.OpenRead(filename))
                {
                    // extract all files from the zip file to the same directory
                    archive.ExtractToDirectory(directory);
                }
            }
        }
    }
}
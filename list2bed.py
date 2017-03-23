import pybedtools, shutil, os, argparse


def ListToBed(inFile, outFile, sort):
    outFileSort = outFile+".srt"
    outHandle = open(outFileSort,"w")
    if(os.stat(inFile).st_size == 0):
        outHandle.write("1\t963754\t963902\n")
    else:
        with open(inFile,'r') as filecontent:
            for line in filecontent:
                data = line.rstrip('\n').split(":")
                chr = data[0]
                if "-" in data[1]:
                    (st,en) = data[1].split("-")
                else:
                    st = data[1]
                    en = int(data[1]) + 1
                outHandle.write(str(chr) + "\t" + str(st) + "\t" + str(en) + "\n")
    outHandle.close()
    if(sort) :
        bedtool = pybedtools.BedTool(outFileSort)
        stbedtool = bedtool.sort()
        mbedtool = stbedtool.merge(d=50)
        c = mbedtool.saveas(outFile)
    else:
        shutil.move(outFileSort, outFile)
    return(outFile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="picard interval list", required=True)
    parser.add_argument("-o", "--output_file", help="output bed file", required=True)
    parser.add_argument("-ns", "--no_sort", help="sort bed file output", default='store_false')
    args = parser.parse_args()
    ListToBed(args.input_file, args.output_file, not args.no_sort)

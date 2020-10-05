import ROOT as r
import argparse
r.gROOT.SetBatch(True)
clock = r.TStopwatch()
clock.Start()

r.gStyle.SetOptStat(0)
import CMS_lumi, tdrstyle
tdrstyle.setTDRStyle() 

#def getBasicParser():
#	parser = argparse.ArgumentParser()
#	parser.add_argument('-v', '--tree_var', type=str, required=False, default="LHE_MothInfo_mtWLep",
#			    help="Variable name in root tree")
#	return parser
ap = argparse.ArgumentParser()
ap.add_argument("-fsm", "--file_SM", type=str, required=True, default="/eos/cms/store/user/jlawhorn/WVJJTree_Jul20/2018/WplusToLNuWplusTo2JJJ_EWK_LO_SM_MJJ100PTJ10_TuneCP5_13TeV-madgraph-pythia8.root", help="SM file path")
ap.add_argument("-faQGC", "--file_aQGC", type=str, required=True, default="/eos/cms/store/user/jlawhorn/WVJJTree_Jul20/2018/WplusTo2LWplusTo2JJJ_EWK_LO_aQGC_MJJ100PTJ10_TuneCP5_13TeV-madgraph-pythia8.root", help="aQGC file path")
ap.add_argument("-v", "--tree_var", type=str, required=True, default="LHE_MothInfo_mtWLep", help="Variable name in root tree")
ap.add_argument("--ofname", type=str, required=False, default="Unknown", help="output file name")
ap.add_argument("--X_SM", type=str, required=False, default="0.039", help="SM sample cross section")
ap.add_argument("--X_aQGC", type=str, required=False, default="0.2223", help="aQGC sample cross section")
ap.add_argument("--cut", type=str, required=False, default="", help="Cut String")
ap.add_argument("--xmin", type=float, required=False, default="0.0", help="minimum range of histogram")
ap.add_argument("--xmax", type=float, required=False, default="1000.0", help="maximum range of histogram")
ap.add_argument("--nbin", type=int, required=False, default="20", help="number of bins in histogramam")
args = ap.parse_args()
print args.tree_var
#print args['tree_var']
def createRatio(h1, h2,col):
    h3 = h1.Clone("h3")
    h3.SetLineColor(col)
    h3.SetMarkerColor(col)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0.0)
    h3.SetMaximum(2.20)
    # Set up plot for markers and errors
    #h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("(SM/Reweighted SM)")
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(15)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitle(args.tree_var+" (GeV)")
    #x.SetTitle("LHE_MothInfo_mtWLep (GeV)")
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4.0)
    x.SetLabelFont(43)
    x.SetLabelSize(15)

    return h3

def createCanvasPads():
    c = r.TCanvas("c", "canvas", 600, 700)
    # Upper histogram plot is pad1
    pad1 = r.TPad("pad1", "pad1", 0.0, 0.3, 1.0, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetLeftMargin(0.1)
    pad1.SetRightMargin(0.03)
    pad1.SetLogy(1)
    pad1.SetGridx()
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = r.TPad("pad2", "pad2", 0.0, 0.00, 1.0, 0.3)
    #pad2.SetLogy(1)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.25)
    pad2.SetLeftMargin(0.1)
    pad2.SetRightMargin(0.03)
    pad2.SetGridx()
    pad2.SetTickx(1)
    pad2.SetTicky(1)
    pad2.Draw()

    return c, pad1, pad2

#canvas = r.TCanvas() 
#canvas.SetLogy(1)
#canvas.SetTickx(1)
#canvas.SetTicky(1) 
#canvas.SetGrid()

#leg = r.TLegend(0.6,0.65,0.9,0.9)
leg = r.TLegend(0.1,0.1,0.4,0.3)
#file_SM = "/eos/cms/store/user/jlawhorn/WVJJTree_Jul20/2018/WplusToLNuWplusTo2JJJ_EWK_LO_SM_MJJ100PTJ10_TuneCP5_13TeV-madgraph-pythia8.root"
#file_aQGC = "/eos/cms/store/user/jlawhorn/WVJJTree_Jul20/2018/WplusTo2LNuWplusTo2JJJ_EWK_LO_aQGC_MJJ100PTJ10_TuneCP5_13TeV-madgraph-pythia8.root"
lumi = "59.0"
X_SM = "0.08793"
X_aQGC = "3.451"
process = "WplusToLNuWplusTo2JJJ"
# Read three fils and their tree
#tfile_SM = r.TFile(file_SM)
tfile_SM = r.TFile(args.file_SM)
#tfile_OnlyFT1_initialize = r.TFile(file_aQGC)
tfile_OnlyFT1_initialize = r.TFile(args.file_aQGC)

tree_OnlyFT1_initialize = tfile_OnlyFT1_initialize.Get("Events")
tree_SM = tfile_SM.Get("Events")
n_aQGC = tree_OnlyFT1_initialize.GetEntries()
n_SM = tree_SM.GetEntries()
print n_SM
print n_aQGC
# See which weights we are going to apply
for n, event in enumerate(tree_OnlyFT1_initialize):
	if n>1:
		break
	print "Weight Details for OnlyFT1_initialize: ID = ",event.aqgcWeight[35],"\tWeight = ",event.aqgcWeight[35]

# Define 3 histogram for three different samples
## Hist 1
print "Reading Histo: h_OnlyFT1_initialize..."
h_OnlyFT1_initialize = r.TH1F("h_OnlyFT1_initialize","",args.nbin,args.xmin,args.xmax)
h_OnlyFT1_initialize.GetXaxis().SetTitle("mT (WW) GeV")
ylabel = "Events / %s GeV" % int(h_OnlyFT1_initialize.GetBinWidth(1))
h_OnlyFT1_initialize.GetYaxis().SetTitle(ylabel)
h_OnlyFT1_initialize.SetLineColor(1)
h_OnlyFT1_initialize.SetMarkerColor(1)
leg.AddEntry(h_OnlyFT1_initialize,"aQGC FT1=1.0","lpe")

## Hist 2
print "Reading Histo: h_aQGC_initialize..."
h_aQGC_initialize = r.TH1F("h_aQGC_initialize","",args.nbin,args.xmin,args.xmax)
h_aQGC_initialize.GetXaxis().SetTitle("mT (WW) GeV")
ylabel = "Events / %s GeV" % int(h_OnlyFT1_initialize.GetBinWidth(1))
h_aQGC_initialize.GetYaxis().SetTitle(ylabel)
h_aQGC_initialize.SetLineColor(2)
h_aQGC_initialize.SetMarkerColor(2)
leg.AddEntry(h_aQGC_initialize,"Reweighted SM (FT1=0.0)","lpe")

## Hist 4
h_SM = r.TH1F("h_SM","",args.nbin,args.xmin,args.xmax)
h_SM.Sumw2()
h_SM.SetLineColor(5)
h_SM.SetMarkerColor(5)
leg.AddEntry(h_SM,"SM","lpe")

print "reading tree : 1"
aQGC = args.tree_var+">>h_aQGC_initialize"
Reweight = args.tree_var+">>h_OnlyFT1_initialize"
SM = args.tree_var+">>h_SM"
#FT5 = args.tree_var+">>h_FT5_12e12"
#if(vbf1_AK4_pt > 50):

tree_OnlyFT1_initialize.Draw(Reweight,args.X_aQGC+"*"+lumi+"*aqgcWeight[26]/"+str(n_aQGC)+"*"+"("+args.cut+")","")
tree_OnlyFT1_initialize.Draw(aQGC,args.X_aQGC+"*"+lumi+"*aqgcWeight[0]/"+str(n_aQGC)+"*"+"("+args.cut+")","")
tree_SM.Draw(SM,args.X_SM+"*"+lumi+"/"+str(n_SM)+"*"+"("+args.cut+")","")
#else:
#print "condition not satisfied"

#h_aQGC_initialize.Scale(1.0/h_aQGC_initialize.Integral())
#h_FT5_12e12.Scale(1.0/h_FT5_12e12.Integral())
#h_OnlyFT1_initialize.Scale(1.0/h_OnlyFT1_initialize.Integral())
#h_SM.Scale(1.0/h_SM.Integral())
#h_AllaQGCPar_initialize.Scale(1.0/h_AllaQGCPar_initialize.Integral())

h3 = createRatio(h_SM,h_aQGC_initialize,1)
#h3 = createRatio(h_SM,h_OnlyFT1_initialize,1)

canvas, pad1, pad2 = createCanvasPads()

#print "Integral h_OnlyFT1_initialize = ",h_OnlyFT1_initialize.Integral()
#print "Integral h_AllaQGCPar_initialize = ",h_AllaQGCPar_initialize.Integral()
#print "Integral h_SM = ",h_SM.Integral()

# Draw all hitogram using sames.
pad1.cd()
h_OnlyFT1_initialize.Draw()
h_SM.Draw("same")
h_aQGC_initialize.Draw("same")
#h_FT5_12e12.Draw("same")
#h_AllaQGCPar_initialize.Draw("same")

leg.Draw()

pad2.cd()
h3.Draw("ep")
#h4.Draw("ep same")
l = r.TLine( 0, 1, 2000, 1 )
l.SetLineStyle(3)
l.Draw("same")

#canvas.Draw()
canvas.SaveAs(args.tree_var+"_"+args.ofname+"_2018.png")

clock.Stop()

print 'Tree loop profiling stats:'
print 'Real Time used:', clock.RealTime()
print 'CPU Time used:', clock.CpuTime()


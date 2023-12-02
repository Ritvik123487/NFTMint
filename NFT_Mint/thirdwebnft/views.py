
from django.shortcuts import redirect, render, HttpResponse
from . import nftall
from thirdweb.types.nft import NFTMetadataInput 
from io import BytesIO

# Create your views here.


def home(request):
    if request.method == 'POST' and request.FILES['home']:
        name_nft = request.POST.get('name','')
        description_nft = request.POST.get('description','')
        image_nft = request.FILES['home'].file
        image_nft.name = request.POST.get('name','')
        prop = {}

    
        nft_metadata = {
            'name': name_nft,
            'description': description_nft,
            'image': image_nft,
            'properties':prop
        }
        nftall.nft_collection.mint(NFTMetadataInput.from_json(nft_metadata))
        return redirect("success")
   
    return render (request, "index.html",{})

def success():
    return HttpResponse("success")



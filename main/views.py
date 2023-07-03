from django.shortcuts import render, HttpResponse
from .models import data
import json
from django.core.serializers import serialize
from .choices import IITS,BRANCHES,SEAT_TYPES,GENDERS
# Create your views here.
from django.db.models import Avg
from django.core.paginator import Paginator


def upload_csv(request):
    if request.method == 'POST':
        print(request.FILES)
        csv_file = request.FILES['document']
        file_data = csv_file.read().decode('utf-8')
        csv_data = file_data.split('\n')
        for x in csv_data:
            fields = x.split(',')
            print(fields)
            info = data(institute=fields[1], program=fields[2], seat_type=fields[3], gender=fields[4], opening_rank=fields[5],
                        closing_rank=fields[6], year=fields[7], roundNo=fields[8], institute_type=fields[10])
            info.save()
    return render(request, 'main/upload.html')

def printdata(request):
    # alldata = data.objects.filter(institute='Indian Institute of Technology Guwahati').all()

    # jsdata = alldata.values('year','closing_rank','roundNo','program')
    # jsdata = list(jsdata)
    # jsdata = json.dumps(jsdata)
    context = {
        'colleges':IITS,
        'branches':BRANCHES,
        'seat_types':SEAT_TYPES,
        'genders':GENDERS,
    }
    if request.method == 'POST':
        seat_type = request.POST.get('seat_type')
        institute = request.POST.get('college_name')
        branch_name = request.POST.get('branch_name')
        gender = request.POST.get('gender')
        alldata = data.objects.filter(seat_type=seat_type,institute=institute,gender=gender,program=branch_name).all()

        jsdata = alldata.values('year','closing_rank','roundNo','program')
        jsdata = list(jsdata)
        jsdata = json.dumps(jsdata)
        context1 = {
            'colleges':IITS,
            'branches':BRANCHES,
            'seat_types':SEAT_TYPES,
            'genders':GENDERS,
            'alldata':alldata,
            'jsdata':jsdata}
        return render(request, 'main/index.html',context1)
        


    return render(request, 'main/index.html',context)



def dig_q1(request):
    popular_branches = [
        'Computer Science and Engineering (4 Years Bachelor of Technology)',
        'Electrical Engineering (4 Years Bachelor of Technology)',
        'Mechanical Engineering (4 Years Bachelor of Technology)',
        'Mathematics and Computing (4 Years Bachelor of Technology)',
        ]
    filtered_data = data.objects.filter(roundNo='6',seat_type='OPEN',gender='Gender-Neutral',program__in=popular_branches)

    jsdata = filtered_data.values('institute','year','program','opening_rank','closing_rank')
    jsdata = json.dumps(list(jsdata))
    context = {
        'alldata':filtered_data,
        'jsdata':jsdata,
    }

    return render(request, 'main/digvijay_q1.html',context)

def Moh_q1(request):
    new_iits = [
        # Add more New IITs as needed
    'Indian Institute of Technology Gandhinagar', 
    'Indian Institute of Technology Jodhpur',
    'Indian Institute of Technology Patna',
    'Indian Institute of Technology Mandi',
    'Indian Institute of Technology Palakkad',
    'Indian Institute of Technology Ropar',
    'Indian Institute of Technology Jammu',
    'Indian Institute of Technology Goa',
    'Indian Institute of Technology Bhilai',
    'Indian Institute of Technology (ISM) Dhanbad',
    'Indian Institute of Technology Tirupati',
    ]

    old_iits = [
    'Indian Institute of Technology Bombay',
        # Add more Old IITs as needed
    'Indian Institute of Technology Delhi',
    'Indian Institute of Technology Kanpur',
    'Indian Institute of Technology Madras',
    'Indian Institute of Technology Kharagpur',
    'Indian Institute of Technology Roorkee',
    'Indian Institute of Technology Guwahati',
    ]

    # Retrieve the unique years from the data
    years = data.objects.values_list('year', flat=True).distinct()

    # Calculate the average closing rank for each year for New IITs
    new_iit_avg_ranks = []
    for year in years:
        new_iit_data = data.objects.filter(
            roundNo='6',
            seat_type='OPEN',
            gender='Gender-Neutral',
            institute__in=new_iits,
            program='Computer Science and Engineering (4 Years Bachelor of Technology)',
            year=year
        ).aggregate(avg_closing_rank=Avg('closing_rank'))
        new_iit_avg_ranks.append({
            'year': year,
            'avg_closing_rank': new_iit_data['avg_closing_rank']
        })

    # Calculate the average closing rank for each year for Old IITs
    old_iit_avg_ranks = []
    for year in years:
        old_iit_data = data.objects.filter(
            roundNo='6',
            seat_type='OPEN',
            gender='Gender-Neutral',
            institute__in=old_iits,
            program='Computer Science and Engineering (4 Years Bachelor of Technology)',
            year=year
        ).aggregate(avg_closing_rank=Avg('closing_rank'))
        old_iit_avg_ranks.append({
            'year': year,
            'avg_closing_rank': old_iit_data['avg_closing_rank']
        })

    # Convert the data to JSON format
    new_iit_json_data = json.dumps(new_iit_avg_ranks)
    old_iit_json_data = json.dumps(old_iit_avg_ranks)
    print(years)
    print(new_iit_json_data)
    print(old_iit_json_data)
    context = {
        'years': years,
        'new_iit_data': new_iit_json_data,
        'old_iit_data': old_iit_json_data,
    }

    return render(request, 'main/mohit_q1.html', context)

def Moh_q1exp(request):
    new_iits = [
        'Indian Institute of Technology Dharwad',
        # Add more New IITs as needed
        'Indian Institute of Technology Gandhinagar', 
    'Indian Institute of Technology Jodhpur',
    'Indian Institute of Technology Patna',
    'Indian Institute of Technology Mandi',
    'Indian Institute of Technology Palakkad',
    'Indian Institute of Technology Ropar',
    'Indian Institute of Technology Jammu',
    'Indian Institute of Technology Goa',
    'Indian Institute of Technology Bhilai',
    'Indian Institute of Technology (ISM) Dhanbad',
    'Indian Institute of Technology Tirupati',
    ]

    # Initialize an empty list to store the institute data
    institute_data = []

    # Retrieve the unique years in the data
    years = data.objects.filter(
        roundNo='6',
        seat_type='OPEN',
        gender='Gender-Neutral',
        institute__in=new_iits,
        program='Computer Science and Engineering (4 Years Bachelor of Technology)'
    ).values_list('year', flat=True).distinct().order_by('year')

    # Iterate over each institute
    for institute in new_iits:
        # Filter data for the current institute
        institute_data_queryset = data.objects.filter(
            roundNo='6',
            seat_type='OPEN',
            gender='Gender-Neutral',
            institute=institute,
            program='Computer Science and Engineering (4 Years Bachelor of Technology)'
        ).values('year').annotate(avg_closing_rank=Avg('closing_rank')).order_by('year')

        # Convert the queryset to a list of dictionaries
        institute_data_list = list(institute_data_queryset)

        # Add the institute name and data to the institute_data list
        institute_data.append({
            'name': institute,
            'data': institute_data_list
        })

    # Convert the institute_data to JSON format
    institute_data_json = json.dumps(institute_data)

    context = {
        'institute_data': institute_data_json,
    }

    return render(request, 'main/mohit_q1exp.html', context)


def Moh_q1exp2(request):
    old_iits = [
          'Indian Institute of Technology Bombay',
        # Add more Old IITs as needed
    'Indian Institute of Technology Delhi',
    'Indian Institute of Technology Kanpur',
    'Indian Institute of Technology Madras',
    'Indian Institute of Technology Kharagpur',
    'Indian Institute of Technology Roorkee',
    'Indian Institute of Technology Guwahati',
    ]

    # Initialize an empty list to store the institute data
    institute_data = []

    # Retrieve the unique years in the data
    years = data.objects.filter(
        roundNo='6',
        seat_type='OPEN',
        gender='Gender-Neutral',
        institute__in=old_iits,
        program='Computer Science and Engineering (4 Years Bachelor of Technology)'
    ).values_list('year', flat=True).distinct().order_by('year')

    # Iterate over each institute
    for institute in old_iits:
        # Filter data for the current institute
        institute_data_queryset = data.objects.filter(
            roundNo='6',
            seat_type='OPEN',
            gender='Gender-Neutral',
            institute=institute,
            program='Computer Science and Engineering (4 Years Bachelor of Technology)'
        ).values('year').annotate(avg_closing_rank=Avg('closing_rank')).order_by('year')

        # Convert the queryset to a list of dictionaries
        institute_data_list = list(institute_data_queryset)

        # Add the institute name and data to the institute_data list
        institute_data.append({
            'name': institute,
            'data': institute_data_list
        })

    # Convert the institute_data to JSON format
    institute_data_json = json.dumps(institute_data)

    context = {
        'institute_data': institute_data_json,
    }

    return render(request, 'main/mohit_q1exp2.html', context)



def branch_popularity(request):
    # Retrieve the unique years in the data
    years = data.objects.values_list('year', flat=True).distinct().order_by('year')

    # Retrieve all branch data
    all_branches = data.objects.values('program').distinct()

    # Initialize the paginator with the all_branches queryset and number of branches per page
    paginator = Paginator(all_branches, 10)

    # Get the current page number from the request query parameters
    page_number = request.GET.get('page')
    
    # Get the branches for the current page
    branches = paginator.get_page(page_number)

    # Initialize an empty list to store the branch data
    branch_data = []

    # Iterate over each branch
    for branch in branches:
        # Filter data for the current branch
        branch_data_queryset = data.objects.filter(program=branch['program']).values('year').annotate(avg_closing_rank=Avg('closing_rank')).order_by('year')

        # Convert the queryset to a list of dictionaries
        branch_data_list = list(branch_data_queryset)

        # Add the branch name and data to the branch_data list
        branch_data.append({
            'name': branch['program'],
            'data': branch_data_list
        })

    # Convert the branch_data to JSON format
    branch_data_json = json.dumps(branch_data)

    context = {
        'branch_data': branch_data_json,
        'years': json.dumps(list(years)),  # Convert years to JSON format
        'branches': branches,  # Pass the paginated branches to the template
    }

    return render(request, 'main/branch_popularity.html', context)



from django.http import JsonResponse
from django.shortcuts import redirect, render

from user.models import CustomUser
from products.models import Variant
from . models import Review
from django.contrib import messages
from user.views import is_user_authenticated,user_passes_test



#add reviews
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def add_review(request,variant_id):

    
    if request.method == 'POST':
        
        if request.POST['star_rating'] == '':
            messages.error(request,'Give rating also')
            return redirect('user:product',id=variant.id)


        if request.POST['review'] == '':
            messages.error(request,'Give review, Cannot leave empty')
            return redirect('user:product',id=variant.id)
        
        user = request.user
        variant = Variant.objects.get(id=variant_id)
        #review object
        review_object = Review(user=user,variant=variant,review=request.POST['review'],
        star_rating=int(request.POST['star_rating'])*20)
        
        review_object.save()
        return redirect('user:product',id=variant.id)
    

#delete review
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def delete_review(request,id,variant_id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('user:product',id=variant_id)


#update review
def update_review(request,id,variant_id):
    try:
        star_rating = request.GET.get('star_rating',None)
        review_value = request.GET.get('review',None)
        review = Review.objects.get(id=id)
        print(review.star_rating)
        if star_rating is not None and review_value is not None:
            review.review = review_value
            review.star_rating = int(star_rating)*20
            review.save()
        print(star_rating,'---------after updation=============',review.star_rating)
         # Return a JSON response indicating success
        return JsonResponse({'message': 'Review updated successfully'})
    except Exception as e:
        # Return a JSON response with an error message
        return JsonResponse({'error': f"Error: {str(e)}"}, status=500)
 
    



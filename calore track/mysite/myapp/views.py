from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Food, Consume


# ---------------- LOGIN ----------------

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'myapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- HOME PAGE ----------------

@login_required(login_url='login')
def index(request):

    foods = Food.objects.all()

    if request.method == "POST":
        food_consumed = request.POST.get('food_consumed')

        food = get_object_or_404(Food, name=food_consumed)

        Consume.objects.create(
            user=request.user,
            food_consumed=food
        )

        return redirect('/')

    consumed_food = Consume.objects.filter(user=request.user)

    # ---------------- SUGGESTION LOGIC ----------------

    total_carbs = 0
    total_protein = 0
    total_fats = 0
    total_calories = 0

    for item in consumed_food:
        total_carbs += item.food_consumed.carbs
        total_protein += item.food_consumed.protein
        total_fats += item.food_consumed.fats
        total_calories += item.food_consumed.calories

    suggestions = []
    recommended_foods = []

    # Calorie Suggestion
    if total_calories == 0:
        suggestions.append("Add food to see health analysis.")
        recommended_foods.append("Start with balanced foods like oats, banana, eggs, dal, and curd.")
    elif total_calories < 1500:
        suggestions.append("⚠ You are eating less than required calories.")
        recommended_foods.append("Add calorie-dense healthy foods: banana, peanut butter, rice, paneer.")
    elif 1500 <= total_calories <= 2200:
        suggestions.append("✅ Your calorie intake is healthy and balanced.")
        recommended_foods.append("Keep your routine with mixed meals: roti/rice + dal + vegetables + protein source.")
    else:
        suggestions.append("🚨 You are consuming excess calories.")
        recommended_foods.append("Prefer lighter foods: salads, sprouts, vegetable soup, grilled options.")

    # Protein Suggestion
    if total_protein < 50:
        suggestions.append("💪 Increase protein intake (eggs, paneer, dal, chicken).")
        recommended_foods.append("Eat more protein foods: eggs, paneer, dal, chickpeas, fish, chicken.")
    elif total_protein > 120:
        suggestions.append("⚠ Excess protein intake.")
        recommended_foods.append("Balance protein with vegetables and whole grains.")
    else:
        suggestions.append("Protein intake is good.")

    # Carbs Suggestion
    if total_carbs > 300:
        suggestions.append("🍚 Reduce high carb foods like rice and sugar.")
        recommended_foods.append("Choose lower-carb options: millets, oats, leafy vegetables, nuts.")
    else:
        suggestions.append("Carbohydrate intake is under control.")

    # Fat Suggestion
    if total_fats > 70:
        suggestions.append("🧈 Limit oily and fried foods.")
        recommended_foods.append("Use healthy fats in small amounts: almonds, walnuts, seeds, olive oil.")
    else:
        suggestions.append("Fat intake is within safe range.")

    dynamic_recommendations = []
    if 0 < total_calories < 1500:
        dynamic_recommendations.extend(
            Food.objects.order_by('-calories').values_list('name', flat=True)[:3]
        )
    elif total_calories > 2200:
        dynamic_recommendations.extend(
            Food.objects.filter(calories__gt=0).order_by('calories').values_list('name', flat=True)[:3]
        )

    if total_protein < 50:
        dynamic_recommendations.extend(
            Food.objects.filter(protein__gte=10).order_by('-protein').values_list('name', flat=True)[:3]
        )
    if total_carbs > 300:
        dynamic_recommendations.extend(
            Food.objects.filter(carbs__lte=20).order_by('carbs').values_list('name', flat=True)[:3]
        )
    if total_fats > 70:
        dynamic_recommendations.extend(
            Food.objects.filter(fats__lte=10).order_by('fats').values_list('name', flat=True)[:3]
        )

    for food_name in dynamic_recommendations:
        message = f"Try: {food_name}"
        if message not in recommended_foods:
            recommended_foods.append(message)

    ai_suggestion = "AI suggestions are currently unavailable. Please check your API key."
    try:
        import os
        from google import genai

        api_key = os.environ.get("GEMINI_API_KEY") or "AIzaSyAh0Qg66Ry1aczBhFGZyrzaEOUzpT1kGwo"
        if api_key:
            client = genai.Client(api_key=api_key)
            prompt = f"I have consumed {total_calories} calories, {total_protein}g protein, {total_carbs}g carbs, and {total_fats}g fats today. Give me one short, helpful, and encouraging sentence of health advice or a food suggestion based on these macros. Do not use markdown."
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            if response.text:
                ai_suggestion = response.text.strip()
    except Exception as e:
        print(f"Error generating AI suggestion: {e}")

    return render(
        request,
        'myapp/index.html',
        {
            'foods': foods,
            'consumed_food': consumed_food,
            'suggestions': suggestions,
            'recommended_foods': recommended_foods,
            'ai_suggestion': ai_suggestion,
        }
    )


# ---------------- DELETE ----------------

@login_required(login_url='login')
def delete_consume(request, id):

    consumed_food = get_object_or_404(
        Consume,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')

    return render(request, 'myapp/delete.html', {'item': consumed_food})
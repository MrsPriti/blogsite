document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-btn');
    const mealList = document.getElementById('meal');
    const mealDetailsContent = document.querySelector('.meal-details-content');
    const searchInput = document.getElementById('recipe-search-input');
    const modalOverlay = document.getElementById('modalOverlay');
    const modal = document.querySelector('.meal-details');

    if (!searchBtn || !searchInput || !mealList) return;

    searchBtn.addEventListener('click', () => getMealList());
    mealList.addEventListener('click', getMealRecipe);

    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') getMealList();
    });

    // Global close function
    window.closeRecipeModal = () => {
        modal.style.display = 'none';
        modalOverlay.style.display = 'none';
        document.body.style.overflow = 'auto';
    };

    // Initial load
    getMealList('');

    function getMealList(query) {
        let searchInputTxt = query !== undefined ? query : searchInput.value.trim();
        
        const stickyEgg = document.getElementById('sticky-easter-egg');
        const eggPlayer = document.getElementById('easter-egg-player');

        // Easter Egg for Chicken
        if (searchInputTxt.toLowerCase() === 'chicken') {
            M.toast({html: '🍗 Winner Winner, Chicken Dinner! 🍗', displayLength: 4000, classes: 'orange darken-4 rounded'});
            document.querySelector('.food-hero').style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => { document.querySelector('.food-hero').style.animation = ''; }, 500);
            
            // Show sticky chicken
            if (stickyEgg && eggPlayer) {
                eggPlayer.load("/static/lottie/chicken.json");
                stickyEgg.style.display = 'block';
            }
        }
        // Easter Egg for Paneer
        else if (searchInputTxt.toLowerCase() === 'paneer') {
            M.toast({html: '🧀 Paneer is not just food, it is an emotion! ✨', displayLength: 4000, classes: 'green darken-3 rounded'});
            document.querySelector('.food-hero').style.animation = 'pulse 0.6s ease-in-out';
            setTimeout(() => { document.querySelector('.food-hero').style.animation = ''; }, 600);

            // Show sticky paneer
            if (stickyEgg && eggPlayer) {
                eggPlayer.load("/static/lottie/paneer.json");
                stickyEgg.style.display = 'block';
            }
        }
        else {
            // Hide sticky egg for other searches
            if (stickyEgg) stickyEgg.style.display = 'none';
        }

        mealList.innerHTML = '<div class="col s12 center-align"><div class="preloader-wrapper active"><div class="spinner-layer spinner-orange-only"><div class="circle-clipper left"><div class="circle"></div></div><div class="gap-patch"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div></div>';

        fetch(`https://www.themealdb.com/api/json/v1/1/search.php?s=${searchInputTxt}`)
        .then(response => response.json())
        .then(data => {
            let html = "";
            if(data.meals){
                data.meals.forEach((meal, index) => {
                    html += `
                        <div class="col s12 m6 l4" style="margin-bottom: 40px; animation: fadeIn 0.5s ease forwards ${index * 0.1}s; opacity: 0;">
                            <div class="recipe-card" data-id="${meal.idMeal}">
                                <div class="recipe-image">
                                    <img src="${meal.strMealThumb}" alt="${meal.strMeal}">
                                </div>
                                <div style="padding: 30px; text-align: center;">
                                    <span style="color: #ea580c; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 10px;">${meal.strCategory}</span>
                                    <h5 style="font-family: 'Playfair Display', serif; font-weight: 800; color: #1e293b; margin: 0 0 25px 0; min-height: 3.5rem; display: flex; align-items: center; justify-content: center;">${meal.strMeal}</h5>
                                    <button class="recipe-btn btn" style="background: #ea580c !important; border-radius: 50px; text-transform: none; font-weight: 700; width: 100%; height: 50px; box-shadow: 0 10px 20px rgba(234, 88, 12, 0.1);">Get Recipe</button>
                                </div>
                            </div>
                        </div>
                    `;
                });
            } else {
                html = '<div class="col s12 center-align"><h4 style="color: #64748b;">Oops! No recipes found for "' + searchInputTxt + '"</h4></div>';
            }
            
            mealList.innerHTML = html;
            
            // Scroll to results if searching
            if (searchInputTxt) {
                const title = document.querySelector('.section-title');
                if (title) title.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        })
        .catch(err => {
            console.error(err);
            mealList.innerHTML = '<div class="col s12 center-align red-text">Connection error. Please try again.</div>';
        });
    }

    function getMealRecipe(e){
        e.preventDefault();
        if(e.target.classList.contains('recipe-btn')){
            let mealId = e.target.closest('.recipe-card').dataset.id;
            fetch(`https://www.themealdb.com/api/json/v1/1/lookup.php?i=${mealId}`)
            .then(response => response.json())
            .then(data => mealRecipeModal(data.meals));
        }
    }

    function mealRecipeModal(meal){
        meal = meal[0];
        
        // Extract ingredients
        let ingredients = [];
        for(let i=1; i<=20; i++){
            if(meal[`strIngredient${i}`]){
                ingredients.push(`${meal[`strIngredient${i}`]} - ${meal[`strMeasure${i}`]}`);
            } else break;
        }

        mealDetailsContent.innerHTML = `
            <div class="row" style="margin: 0;">
                <div class="col s12 l5" style="padding: 0; height: 100%;">
                    <img src="${meal.strMealThumb}" style="width: 100%; height: 100%; object-fit: cover; min-height: 400px;">
                </div>
                <div class="col s12 l7" style="padding: 50px; overflow-y: auto;">
                    <span style="color: #ea580c; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;">${meal.strCategory} | ${meal.strArea}</span>
                    <h2 style="font-family: 'Playfair Display', serif; font-weight: 900; color: #1e293b; margin: 15px 0 30px 0;">${meal.strMeal}</h2>
                    
                    <div style="margin-bottom: 40px;">
                        <h5 style="font-weight: 800; color: #1e293b; margin-bottom: 20px; display: flex; align-items: center;">
                            <i class="fas fa-list" style="margin-right: 15px; color: #ea580c;"></i> Ingredients
                        </h5>
                        <ul style="column-count: 2; list-style: none; padding: 0;">
                            ${ingredients.map(ing => `<li style="margin-bottom: 10px; color: #64748b; font-size: 0.95rem;">• ${ing}</li>`).join('')}
                        </ul>
                    </div>

                    <div style="margin-bottom: 40px;">
                        <h5 style="font-weight: 800; color: #1e293b; margin-bottom: 20px; display: flex; align-items: center;">
                            <i class="fas fa-utensils" style="margin-right: 15px; color: #ea580c;"></i> Instructions
                        </h5>
                        <p style="line-height: 1.8; color: #475569; font-size: 1.05rem; text-align: justify;">${meal.strInstructions}</p>
                    </div>

                    <div class="center-align">
                        <a href="${meal.strYoutube}" target="_blank" class="btn red darken-1" style="border-radius: 50px; height: 55px; line-height: 55px; padding: 0 40px; text-transform: none; font-weight: 700; font-size: 1.1rem;">
                            <i class="fab fa-youtube" style="margin-right: 10px;"></i> Watch Video Tutorial
                        </a>
                    </div>
                </div>
            </div>
        `;
        
        modal.style.display = 'block';
        modalOverlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
});

// Keyframe animation for cards
const style = document.createElement('style');
style.innerHTML = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);
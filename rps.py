import random  
import cv2  
import cvzone  
from cvzone.HandTrackingModule import HandDetector  
import time 
import webbrowser

cap = cv2.VideoCapture(0)  # Open the webcam (device 0 is usually the default)
cap.set(3, 640)  # Set the width of the captured frame to 640 pixels
cap.set(4, 480)  # Set the height of the captured frame to 480 pixels

detector = HandDetector(maxHands=1)  # Initialize the hand detector, limiting to detecting one hand at a time

timer = 0  # Initialize the timer variable to 0, used to keep track of the elapsed time
stateResult = False  # Initialize the game result state to False, meaning the game is ongoing
startGame = False  # Boolean flag to indicate whether the game has started or not
scores = [0, 0]  # List to keep track of scores, where scores[0] is the AI score, and scores[1] is the player's score
imgEmoji = cv2.resize(cv2.imread("Resources/smile.png", cv2.IMREAD_UNCHANGED), (50, 50)) 
imgAI = cv2.resize(cv2.imread("Resources/oct.png", cv2.IMREAD_UNCHANGED), (500, 350))

while True:  # Infinite loop to keep the game running
    imgBG = cv2.resize(cv2.imread("Resources/water3.png"), (900, 950))   # Read the background image for the game
    imgBaG = cv2.resize(cv2.imread("Resources/water3.png"), (900, 950))   # Read the background image for the game
    success, img = cap.read()  # Capture a frame from the webcam
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)  # Scale down the captured frame by 87.5%
    imgScaled = imgScaled[:, 100:500] # Crop the scaled image to focus on the center portion
    imgBG = cvzone.overlayPNG(imgBG, imgAI, (49, 110)) 

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # Detect hands in the scaled image and draw landmarks
    if hands:  # If hands are detected
        hand = hands[0]
        fingers = detector.fingersUp(hand) 
        
        # Determine the player's move based on the fingers
        if fingers == [0, 0, 0, 0, 0]:
            imgEmoji = cv2.resize(cv2.imread("Resources/rock.png", cv2.IMREAD_UNCHANGED), (50, 50))
        elif fingers == [1, 1, 1, 1, 1]:
            imgEmoji = cv2.resize(cv2.imread("Resources/paper.png", cv2.IMREAD_UNCHANGED), (50, 50))
        elif fingers == [0, 1, 1, 0, 0]:
            imgEmoji = cv2.resize(cv2.imread("Resources/scissors.png", cv2.IMREAD_UNCHANGED), (50, 50))
        else:
            imgEmoji = cv2.resize(cv2.imread("Resources/smile.png", cv2.IMREAD_UNCHANGED), (50, 50))

    if startGame:  # If the game has started
        if stateResult is False:  # If the result state is False (game is still ongoing)
            timer = time.time() - initialTime  # Calculate the elapsed time since the game started
            # Display the timer on the background image at position (605, 435)
            cv2.putText(imgBG, str(int(timer)), (405, 535), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:  # If the timer exceeds 3 seconds, the round is over
                stateResult = True  # Set the result state to True (indicating the round is over)
                timer = 0  # Reset the timer

                if hands:  # If hands are detected
                    playerMove = None  # Initialize the player's move variable
                    hand = hands[0]  # Get the first detected hand
                    fingers = detector.fingersUp(hand)  # Get the list of fingers that are up on the hand

                    # Determine the player's move based on the fingers
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Scissors    

                    randomNumber = random.randint(1, 3)  # AI randomly picks a move (1: Rock, 2: Paper, 3: Scissors)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)  # Load AI's move image
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (649, 810))  # Overlay the AI move image onto the background

                    # Check if the player wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1  # Increment the player's score

                    # Check if the AI wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1  # Increment the AI's score
                        
                    # Check if anyone reached a score of 3, ending the game
                    if scores[0] == 3 or scores[1] == 3:
                        imgBG = cv2.resize(cv2.imread("Resources/water3.png"), (900, 950))
                        cv2.putText(imgBG, "Game Over!", (320, 420), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 6)
                        cv2.putText(imgBG, f"Winner: {'AI' if scores[0] == 3 else 'Player'}", (230, 480), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 6)
                        cv2.imshow("BG", imgBG)
                        cv2.waitKey(3000)  # Wait for 3 seconds before exiting
                        startGame = False  # Stop the game after it ends
                        scores = [0, 0]  # Reset the scores after game over
                        imgBG = cv2.resize(cv2.imread("Resources/water3.png"), (900, 950))
                        cv2.putText(imgBG, "Etes-vous interesses par l'ecole ?", (100, 200), 
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
                        cv2.putText(imgBG, "Oui (Appuyez sur 'o') / Non (Appuyez sur 'n')", (100, 400),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
                        cv2.imshow("BG", imgBG)

                        # Wait for a key press to capture the response
                        key = cv2.waitKey(0)  # Wait indefinitely until a key is pressed

                        # Respond to the input
                        if key == ord('o'):  # 'o' for Oui
                            print("Redirection vers le document d'inscription...")
                            # Open the enrollment document (e.g., PDF or webpage)
                            webbrowser.open("https://www.ia-institut.fr/ecole-intelligence-artificielle/rdv-personnalise/")  # Replace with actual URL or file path
                        elif key == ord('n'):  # 'n' for Non
                            print("Redirection vers Kraken...")
                            # Open Kraken (or any other website)
                            continue  # Continue the loop to reset the game
 # Replace with the actual Kraken URL or destination
                        

    # Overlay the webcam feed (scaled and cropped) onto the background at the bottom-right corner
    imgBG[530:950, 500:900] = imgScaled
    imgBG = cvzone.overlayPNG(imgBG, imgEmoji, (500, 860))

    if stateResult:  # If the result state is True (round has ended)
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (49, 110))  # Overlay the AI move image again

    # Display the AI and player scores on the background image
    cv2.putText(imgBG, str(scores[0]), (110, 85), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)  # AI's score
    cv2.putText(imgBG, str(scores[1]), (612, 85), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)  # Player's score

    # Display the background image with the updated information
    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)  # Wait for a key press
    if key == ord('s'):  # If the 's' key is pressed, start the game
        startGame = True  # Set the game state to started
        initialTime = time.time()  # Record the current time as the start time
        stateResult = False  # Set the result state to False for the next round






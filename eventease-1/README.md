# EventEase - Event Management Web Application

EventEase is an event management web application that allows users to create, join, and manage events. The application includes features for volunteer communication through a walkie-talkie functionality using PeerJS, as well as channels for announcements, public messaging, and ticket management.

## Features

- **Event Creation**: Users can create events with unique IDs, descriptions, and participant/volunteer phone numbers.
- **Event Joining**: Participants can join events using their phone numbers and gain access based on their roles.
- **Event Dashboard**: A dedicated dashboard for each event where participants and volunteers can interact.
- **Walkie-Talkie Feature**: Volunteers can communicate in real-time using the walkie-talkie feature powered by PeerJS.
- **Announcements**: Admins can post announcements for all participants.
- **Public Messaging**: Participants can send messages to each other in a public channel.
- **Ticket Management**: Participants can create tickets for issues, and admins can respond to them.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd eventease
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Usage

- Navigate to the home page to create or join events.
- Use the event dashboard to manage event-specific functionalities.
- Access the walkie-talkie feature from the event dashboard for real-time communication.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
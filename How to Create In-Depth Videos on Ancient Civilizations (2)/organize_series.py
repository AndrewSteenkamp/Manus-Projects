import csv
import os

SERIES_MAP = {
    "The Cradles of Civilization": ["Hammurabi's Code: The Dawn of Law", "The Epic of Gilgamesh: Humanity's First Great Story", "Mummification: The Egyptian Obsession with the Afterlife", "Cleopatra: The Last Pharaoh", "The Uncracked Code: The Mystery of the Indus Valley Script", "The Mandate of Heaven: How Chinese Dynasties Justified Their Rule", "The Nazca Lines: Geoglyphs of the Gods"],
    "Empires of the Mediterranean": ["The Birth of Democracy in Athens", "The Spartans: Warriors of the Ancient World", "The Trojan War: Myth or History?", "The Rise of the Roman Republic", "Julius Caesar: The Man Who Would Be King", "The Colosseum: Rome's Arena of Death", "The Phoenicians: Masters of the Sea and the Alphabet", "Carthage: Rome's Greatest Rival", "The Palace of Knossos: Labyrinth of the Minotaur", "The Thera Eruption: The Real Atlantis?", "The Lion Gate of Mycenae: Gateway to a Lost World", "Agamemnon and the Trojan War: The View from the Greek Side"],
    "Mesoamerican Marvels": ["The Maya Calendar: More Than Just 2012", "Tikal: The Great City in the Jungle", "The Collapse of the Maya: What Really Happened?", "Tenochtitlan: The Venice of the New World", "Human Sacrifice: The Dark Side of Aztec Religion", "The Conquest of the Aztec Empire", "Machu Picchu: The Lost City of the Incas", "The Quipu: The Inca's Secret Code", "The Inca Road: Engineering an Empire"],
    "Giants of Asia": ["The Mauryan Empire: Ashoka the Great and the Spread of Buddhism", "The Gupta Empire: The Golden Age of India", "The Jomon Period: Japan's Prehistoric Fishermen", "The Yayoi Period: The Introduction of Rice and Metal", "Angkor Wat: The World's Largest Religious Monument", "The Rise and Fall of the Khmer Empire"],
    "Lost Civilizations": ["The Hittites: The Forgotten Empire of Anatolia", "The Battle of Kadesh: The World's First Recorded Battle", "Petra: The Rose-Red City Half as Old as Time", "The Nabateans: Masters of the Desert Trade", "The Kingdom of Aksum: The African Empire You've Never Heard Of", "The Stelae of Aksum: The Tallest Single Stones Ever Erected by Man"]
}

def get_series_from_topic(topic):
    for series, topics in SERIES_MAP.items():
        if topic in topics:
            return series
    return "Uncategorized"

os.makedirs("/home/ubuntu/series_documents", exist_ok=True)

with open("/home/ubuntu/ancient_civilizations_video_packages_all.csv", "r", newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if len(row) < 3:
            continue
        subject = row[0]
        video_script = row[1]
        pictory_prompts = row[2]
        series = get_series_from_topic(subject)
        series_filename = f"/home/ubuntu/series_documents/{series.replace(' ', '_')}.md"
        with open(series_filename, "a", encoding='utf-8') as series_file:
            series_file.write(f"# {subject}\n\n")
            series_file.write(video_script + "\n\n")
            series_file.write(pictory_prompts + "\n\n---\n\n")

print("Done. Files created:")
for f in os.listdir("/home/ubuntu/series_documents"):
    size = os.path.getsize(f"/home/ubuntu/series_documents/{f}")
    print(f"  {f}: {size} bytes")

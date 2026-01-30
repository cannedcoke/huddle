#include <iostream>
#include <list>

using namespace std;

class Fruit// class obv
{
private:// modificador de acceso
    string Name;
    string Color;
    int Sold;
    list<string> Variedades;
public://acess modifier
    Fruit(string name, string color)//constructor
    {
        Name = name;
        Color = color;
        Sold = 0; // cuando creas recien todavia no vendiste nada so se inicializa en cero
    }


    //imprime el objeto
    void GetInfo()
    {
        
        cout << "Fruta: " << Name << " ,color: " << Color << ", cantidad: " << Sold << endl;
        cout << "veriedades disponibles: ";
        for (string vairedad : Variedades)
        {
            cout << vairedad << endl;
        }
    }

    void compra(){
        Sold++;
    }
    void returned(){
        Sold--;
    }
};

int main()
{
    //object
    Fruit fruta("apple", "green");
    fruta.compra();
    // fruta.Variedades.push_back("red");
    // Fruit fruta2("orange","red");
    fruta.GetInfo();

    return 0;
}

bool start_goal(vector<vector<int>> &maze, int width, int height, int start_x, int start_y, int end_x, int end_y)
{

    if (inside(maze, width, height, start_x, start_y) && inside(maze, width, height, end_x, end_y))
    {
        maze[start_y][start_x] = 5;
        maze[end_y][end_x] = 6;
        return false;
    }
    else
    {
        cout << "coordenadas invalidas, intente de nuevo ";
        return true;
    }
}

class Marker{

    


};
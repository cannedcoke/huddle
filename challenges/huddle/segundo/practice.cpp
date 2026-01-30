#include <vector>
#include <iostream>
using namespace std;

const int MAX = 100;
// voy a hacer una clase llamada notas
//  en provate un vector notas que se va a  inicializar con n

class Notas
{
private:
    int n;
    vector<int> grade;

public:
    Notas(int n) : n(n), grade(n) {}

    int size() const
    {
        return grade.size();
    }

    void cargarNotas()
    {
        for (size_t i = 0; i < grade.size(); i++)
        {
            int notas;
            cout << "Nota " << i + 1 << ": ";
            cin >> notas;
            grade[i] = notas;
        }
    }

    double promedio()
    {
        int suma = 0;
        for (size_t i = 0; i < grade.size(); i++)
            suma += grade[i];

        return (double)suma / n;
    }

    int notaMax()
    {
        int max = grade[0];
        for (size_t i = 1; i < grade.size(); i++)
            if (grade[i] > max)
                max = grade[i];

        return max;
    }

    int notaMin()
    {
        int min = grade[0];
        for (size_t i = 1; i < grade.size(); i++)
            if (grade[i] < min)
                min = grade[i];

        return min;
    }
};

int main()
{
    int n;

    cout << "Cantidad de notas: ";
    cin >> n;
    Notas segundo(n);

    segundo.cargarNotas();

    cout << "Promedio: " << segundo.promedio() << endl;
    cout << "Maxima: " << segundo.notaMax() << endl;
    cout << "Minima: " << segundo.notaMin() << endl;

    return 0;
}
